from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.cargarInicio, name='cargarInicio'),
    path('2_productos/', views.cargarproducto, name='cargarproducto'),
    path('3_menus/', views.cargarmenu, name='cargarmenu'),
    path('4_contacto/', views.cargarcontacto, name='cargarcontacto'),
    path('5_preguntas/', views.cargarpreguntas, name='cargarpreguntas'),
    path('6_nosotros/', views.cargarsomos, name='cargarsomos'),
    path('7_carro/', views.cargarcarro, name='cargarcarro'),
    path('8_sesiones/', auth_views.LoginView.as_view(template_name='8_sesiones.html'), name='login'),
    path('registro/', views.cargarregistro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cargarInicio'), name='logout'),
    path('agregar/<uuid:producto_id>/', views.agregar_al_carro, name='agregar_al_carro'),
    path('eliminar/<uuid:producto_id>/', views.eliminar_del_carro, name='eliminar_del_carro'),
    path('actualizar/<uuid:producto_id>/', views.actualizar_carro, name='actualizar_carro'),
    path('product/<uuid:product_id>/like/', views.like_product, name='like_product'),  
    path('chat/', views.chat_view, name='chat_view'),
    path('formulario/', views.Cargarformulario, name='formulario'),
    path('verificar_stock/', views.verificar_stock, name='verificar_stock'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),


]