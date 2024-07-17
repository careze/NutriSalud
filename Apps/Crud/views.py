from django.shortcuts import render, redirect, get_object_or_404
from .forms import MenuForm, ProductoForm
from .models import Producto, Menu, User, Categoria, Corazon
from django.db.models import Count
import json
from Apps.Home.forms import UserCreationForm
from collections import Counter 
from .models import Categoria 
from django.http import JsonResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def cargar_inicio_crud(request):
    productos = Producto.objects.all()
    menus = Menu.objects.all()
    elementos = [{'obj': prod, 'tipo': 'Producto'} for prod in productos] + [{'obj': menu, 'tipo': 'Menu'} for menu in menus]
    #elementos = list(productos) + list(menus)
    return render(request, "inicioCrud.html", {'elementos': elementos})


def ver_crud(request, id):
    try:
        objeto = get_object_or_404(Producto, pk=id)
        tipo = 'Producto'
        categorias = objeto.categoria.all()
    except Http404:
        objeto = get_object_or_404(Menu, pk=id)
        tipo = 'Menu'
        categorias = objeto.categoria.all()
    return render(request, "verCrud.html", {'objeto': objeto, 'tipo': tipo, 'categorias': categorias})

def eliminar_crud(request, id):
    try:
        objeto = get_object_or_404(Producto, pk=id)
        tipo = 'Producto'
    except Http404:
        objeto = get_object_or_404(Menu, pk=id)
        tipo = 'Menu'
    if request.method == 'POST':
        objeto.delete()
        return redirect('cargar_inicio_crud')
    return render(request, "verCrud.html", {'objeto': objeto, 'tipo': tipo})

def editar_crud(request, id):
    try:
        objeto = get_object_or_404(Producto, pk=id)
        tipo = 'Producto'
        form_class = ProductoForm
    except Http404:
        objeto = get_object_or_404(Menu, pk=id)
        tipo = 'Menu' 
        form_class = MenuForm
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=objeto)
        if form.is_valid():
            form.save()
            return redirect('ver_crud', id=id)
    else:
        form = form_class(instance=objeto)
    
    return render(request, "EditarCrud.html", {'form': form,  'tipo': tipo, 'objeto': objeto})

def crear_crud(request):
    tipo = request.GET.get('tipo','Producto')
    
    if request.method == "POST":
        if tipo == 'Producto':
            form = ProductoForm(request.POST, request.FILES)
        else:
            form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cargar_inicio_crud')    
    else:
        if tipo == 'Producto':
            form = ProductoForm()
        else:
            form = MenuForm()
    return render(request, "CrearCrud.html", {'form': form, 'tipo': tipo})

def metrics_view(request):
    categories = Categoria.objects.all()
    category_counts = []
    age_distribution = []

    for category in categories:
        count = User.objects.filter(categoria=category).count()
        category_counts.append({
            'categoria__nombre': category.nombre,
            'total': count
        })
        users_in_category = User.objects.filter(categoria=category)
        for user in users_in_category:
            age_distribution.append({
                'categoria__nombre': category.nombre,
                'edad': user.edad
            })
    context = {
        'category_counts': json.dumps(category_counts),
        'age_distribution': json.dumps(age_distribution)
    }
    return render(request, 'metrics.html', context)