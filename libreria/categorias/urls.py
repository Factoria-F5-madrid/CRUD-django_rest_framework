from django.urls import path
from .views import VistasCategorias

urlpatterns = [
    path('categorias/', VistasCategorias.ListaCategorias, name='lista-categoria'),
    path('categorias/crear', VistasCategorias.crearCategorias, name='crear-categoria'),
    path('categorias/<int:pk>/', VistasCategorias.DetalleCategorias, name='detalle-categoria'),
]