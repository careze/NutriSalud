from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Apps.Crud.models import Producto, Menu, Corazon, Carrito
from Apps.Home.forms import UserCreationForm
from django.db.models import Q, Count
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
import json
import openai
from openai import ChatCompletion




def cargarInicio(request):
    menus = Menu.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]
    return render(request, "1_inicio.html", {'menus': menus})


def cargarproducto(request):
    productos = Producto.objects.all()
    query = request.GET.get('busqueda')
    if query:
        productos = productos.filter(
            Q(nombreProducto__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(precio__contains=query)
        )
    return render(request, "2_productos.html", {'productos': productos})


def cargarmenu(request):
    menus = Menu.objects.all()
    query = request.GET.get('busqueda', '')
    categoria = request.GET.get('categoria', '')


    if query:
        menus = menus.filter(
            Q(nombreMenu__icontains=query) |
            Q(descripcion__icontains=query)
        )


    if categoria:
        menus = menus.filter(categoria__nombre=categoria)


    return render(request, "3_menus.html", {'menus': menus, 'categoria_seleccionada': categoria, 'busqueda': query})


def cargarcontacto(request):
 return render(request, '4_contacto.html')


def cargarpreguntas(request):
    return render(request, "5_preguntas.html")


def cargarsomos(request):
    return render(request, "6_nosotros.html")


@login_required
def cargarcarro(request):
    carro = request.session.get('carro', {})
    productos = []
    total = 0


    for item_id, cantidad in carro.items():
        try:
            producto = Producto.objects.get(id=item_id)
            nombre = producto.nombreProducto
        except Producto.DoesNotExist:
            try:
                producto = Menu.objects.get(id=item_id)
                nombre = producto.nombreMenu
            except Menu.DoesNotExist:
                continue
       
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({'producto': producto, 'nombre': nombre, 'cantidad': cantidad, 'subtotal': subtotal})
   
    return render(request, '7_carro.html', {'productos': productos, 'total': total})


def agregar_al_carro(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carro = request.session.get('carro', {})
        carro[str(producto_id)] = carro.get(str(producto_id), 0) + cantidad  
        request.session['carro'] = carro
        print("Producto agregado al carrito:", producto_id, "Cantidad:", cantidad)
        print("Contenido del carro:", request.session['carro'])  
    return redirect('cargarcarro')


def actualizar_carro(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carro = request.session.get('carro', {})
        carro[str(producto_id)] = cantidad  
        request.session['carro'] = carro
        print("Producto actualizado en el carrito:", producto_id, "Cantidad:", cantidad)
        print("Contenido del carro:", request.session['carro'])  
    return redirect('cargarcarro')


def eliminar_del_carro(request, producto_id):
    if request.method == 'POST':
        print("Solicitud POST recibida para eliminar producto:", producto_id)
        carro = request.session.get('carro', {})
        if str(producto_id) in carro:  
            del carro[str(producto_id)]  
            request.session['carro'] = carro
            print("Producto eliminado del carrito:", producto_id)
            print("Contenido del carro:", request.session['carro'])  
        else:
            print("El producto no está en el carrito:", producto_id)
    return redirect('cargarcarro')


def cargarsesion(request):
    return render(request, "8_sesiones.html")


def cargarregistro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cargarInicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def like_product(request, product_id):
    menu = get_object_or_404(Menu, id=product_id)
    if menu.likes.filter(user=request.user).exists():
        menu.likes.filter(user=request.user).delete()
    else:
        Corazon.objects.create(menu=menu, user=request.user)


    return redirect('cargarmenu')


def chat_view(request):
    conversation = request.session.get('conversation', [])
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        prompts = []
        if user_input:
            conversation.append({"role": "user", "content": user_input})
        prompts.extend(conversation)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key="sk-proj-lyjLv49kkox3Hh3IYSlTT3BlbkFJxH65AMn2MyGrZYV0IgwT"
        )


        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})
        request.session['conversation'] = conversation


        return render(request, 'chat.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        request.session.clear()
        return render(request, 'chat.html', {'conversation': conversation})

def Cargarformulario(request):
    return render(request, 'forms.html')


def verificar_stock(request):
    carro = request.session.get('carro', {})
    if not carro:
        messages.error(request, "No tienes productos en el carrito.")
        return redirect('cargarcarro')

    stock_insuficiente = []

    for item_id, cantidad in carro.items():
        try:
            producto = Producto.objects.get(id=item_id)
            if producto.stock < cantidad:
                stock_insuficiente.append(producto.nombreProducto)
        except Producto.DoesNotExist:
            try:
                producto = Menu.objects.get(id=item_id)
                if producto.stock < cantidad:
                    stock_insuficiente.append(producto.nombreMenu)
            except Menu.DoesNotExist:
                continue

    if stock_insuficiente:
        mensaje = f"No hay suficiente stock para: {', '.join(stock_insuficiente)}"
        messages.error(request, mensaje)
        return redirect('cargarcarro')

    # Mensaje de depuración
    print("Stock verificado, redirigiendo a procesar_pago")
    # Si todo el stock es suficiente, procede con el pago
    return redirect('procesar_pago')



def procesar_pago(request):
    carro = request.session.get('carro', {})
    if not carro:
        messages.error(request, "No tienes productos en el carrito.")
        return redirect('cargarcarro')

    productos = []
    total = 0

    for item_id, cantidad in carro.items():
        try:
            producto = Producto.objects.get(id=item_id)
            nombre = producto.nombreProducto
        except Producto.DoesNotExist:
            try:
                producto = Menu.objects.get(id=item_id)
                nombre = producto.nombreMenu
            except Menu.DoesNotExist:
                continue
        
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({'producto': producto, 'nombre': nombre, 'cantidad': cantidad, 'subtotal': subtotal})
    
    return render(request, 'procesar_pago.html', {'total': total})

@csrf_exempt
def confirmar_pago(request):
    if request.method == 'POST':
        carro = request.session.get('carro', {})
        for item_id, cantidad in carro.items():
            try:
                producto = Producto.objects.get(id=item_id)
                producto.stock -= cantidad
                producto.save()
            except Producto.DoesNotExist:
                try:
                    producto = Menu.objects.get(id=item_id)
                    producto.stock -= cantidad
                    producto.save()
                except Menu.DoesNotExist:
                    continue
        
        # Limpiar el carrito después de procesar el pago y descontar el stock
        request.session['carro'] = {}
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)