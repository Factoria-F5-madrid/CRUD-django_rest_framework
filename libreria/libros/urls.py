from django.urls import path
from .views import VistasLibros

urlpatterns = [
    path('libros', VistasLibros.ListaLibros, name="Lista_libros"),
    path('libros/crear', VistasLibros.CrearLibros, name="crear_libros"),
    path('libros/<int:pk>', VistasLibros.DetalleLibros, name="detalle_libros"),
]