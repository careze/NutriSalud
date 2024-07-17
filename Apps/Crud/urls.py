from django.urls import path
from . import views

urlpatterns =[
    path('', views.cargar_inicio_crud, name='cargar_inicio_crud'),
    path('crear/', views.crear_crud, name='crear_crud'),
    path('verCrud/<uuid:id>/', views.ver_crud, name='ver_crud'),
    path('eliminarCrud/<uuid:id>/', views.eliminar_crud, name='eliminar_crud'),
    path('editar-crud/<uuid:id>/', views.editar_crud, name='editar_crud'),
    path('metrics/', views.metrics_view, name='metrics'),
]










