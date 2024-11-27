# API CRUD con Django y Django REST Framework

## Índice

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Creación del Modelo](#creación-del-modelo)
5. [Implementación del Serializador](#implementación-del-serializador)
6. [Creación de Vistas API](#creación-de-vistas-api)
7. [Configuración de URLs](#configuración-de-urls)
8. [Prueba de la API](#prueba-de-la-api)
9. [Mejores Prácticas](#mejores-prácticas)
10. [Recursos Adicionales](#recursos-adicionales)

## Introducción

Esta guía te llevará a través del proceso de creación de una API CRUD (Crear, Leer, Actualizar, Eliminar) utilizando Django y Django REST Framework (DRF). Construiremos una API simple para gestionar una lista de libros.

## Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Conocimientos básicos de Django y APIs RESTful

## Configuración del Proyecto

*Recuerda iniciar tu entorno virtual, sea que lo hagas con **"uv venv"** o con **"python -m venv venv"** por ejemplo, y actívalo*

1. Crea un nuevo proyecto Django:

```bash
django-admin startproject libreria
cd libreria
```

2. Crea dos aplicaciones:

```bash
python manage.py startapp libros
```
Y nuevamente:

```bash
python manage.py startapp categorias
```

3. Instala Django REST Framework:

```bash
pip install djangorestframework
```

4. Añade 'rest_framework' y 'libros' a INSTALLED_APPS en settings.py:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'libros',
    'categorias',
]
```

### Esta sería tu estructura
```plaintext
crud_python/ # Carpeta donde guardas tu proyecto
│
├── manage.py
├── libreria/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── libros/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py 
│   ├── views.py
│ 
├── categorias/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py 
│   ├── views.py
│
```

## Conexión a la Base de Datos usando .env

Para proteger información sensible como las credenciales de tu base de datos, es recomendable usar un archivo `.env` para almacenar estas configuraciones de manera segura.

### Instalación de mysqlclient

Debes instalar mysqlclient, que es el adaptador que Django usa para conectarse a MySQL. Puedes hacerlo ejecutando:

```bash
pip install mysqlclient
```

### Instalación de python-dotenv

1. Asegúrate de tener instalado `python-dotenv` para cargar las variables de entorno en tu proyecto:

```bash
pip install python-dotenv
```
2. Configuración del archivo .env

    Crea un archivo `.env` en la raíz de tu proyecto y añade las variables de conexión a tu base de datos:

```env
DB_NAME=nombre_base_de_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost  # o la dirección de tu servidor de base de datos
DB_PORT=3306       # o el puerto que uses (por defecto es 3306 para MySQL)
```
3. Modificación de settings.py

    Actualiza settings.py para que Django cargue estas variables de entorno y configure la conexión a la base de datos:

```python
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()
[...]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Cambia el motor a MySQL
        'NAME': os.getenv('DB_NAME'),          # Nombre de tu base de datos
        'USER': os.getenv('DB_USER'),          # Usuario de tu base de datos
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Contraseña del usuario
        'HOST': os.getenv('DB_HOST'),          # Dirección del servidor de la base de datos (e.g., 'localhost')
        'PORT': os.getenv('DB_PORT'),          # Puerto de la base de datos (por defecto es 3306 para MySQL)
    }
}
```

## Creación del Modelo

En libros/models.py, crea el modelo Libro:

```python
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo
```

En categorias/models.py, crea el modelo Libro:

```python
from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_categoria
```

Ejecuta las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

En Django, debes hacer migraciones cada vez que realizas cambios en los modelos de tu aplicación que afectan la estructura de la base de datos. Las migraciones son archivos que Django utiliza para aplicar estos cambios en la base de datos de manera controlada.

## Implementación del Serializador

Crea libros/serializers.py:

```python
from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'isbn', 'fecha_publicacion']
```

o también podría ser así:

```python
from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
```

Crea categorias/serializers.py:

```python
from rest_framework import serializers
from .models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']
```

## Creación de Vistas API

En libros/views.py, crea vistas para las operaciones CRUD:

```python
from rest_framework import generics
from .models import Libro
from .serializers import LibroSerializer

class ListaLibros(generics.ListCreateAPIView):
    libros = Libro.objects.all()
    serializer = LibroSerializer

class DetalleLibro(generics.RetrieveUpdateDestroyAPIView):
    libro = Libro.objects.all()
    serializer = LibroSerializer
```

o también podría ser así:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Libro
from .serializers import LibroSerializer

class VistasLibros(generics.ListCreateAPIView):
    @api_view(['GET'])
    def ListaLibros(request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    @api_view(['PUT', 'DELETE'])
    def DetalleLibros(request, pk):
        try:
            libro = libro.objects.get(pk=pk)
        except libro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            libro = Libro.objects.get(pk=pk)
            serializer = LibroSerializer(libro)
            if libro.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = LibroSerializer(libro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            libro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
```

En categorias/views.py, crea vistas para las operaciones CRUD:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Categoria
from .serializers import CategoriaSerializer

class VistasCategorias(generics.ListCreateAPIView):
    @api_view(['GET'])
    def ListaCategorias(request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(libros, many=True)
        return Response(serializer.data)

    @api_view(['GET','PUT', 'DELETE'])
    def DetalleCategorias(request, pk):
        try:
            categoria = Categoria.objects.get(pk=pk)
        except categoria.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            categoria = Categoria.objects.get(pk=pk)
            serializer = CategoriaSerializer(categoria)
            if categoria.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = CategoriaSerializer(categoria, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            categoria.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
```

## Configuración de URLs

1. En libros/urls.py (crea este archivo si no existe):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('libros/', views.ListaLibros.as_view(), name='lista-libros'),
    path('libros/<int:pk>/', views.DetalleLibro.as_view(), name='detalle-libro'),
]
```

O también podría ser de esta manera:

```python
from django.urls import path
from .views import ListaLibros, DetalleLibros

urlpatterns = [
    path('libros', ListaLibros, name="Lista_libros"),
    path('libros/<int:pk>', DetalleLibros, name="detalle_libros"),
]
```

Y luego en categorias/urls.py
En libros/urls.py (crea este archivo si no existe):

```python
from django.urls import path
from .views import ListaCategorias, DetalleCategorias

urlpatterns = [
    path('categorias/', ListaCategorias, name='lista-categoria'),
    path('categorias/<int:pk>/', DetalleCategorias, name='detalle-categoria'),
]
```

2. En libreria/urls.py, incluye las URLs de la aplicación libros:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('libros.urls')),
    path('api/', include('categorias.urls')),
]
```

## Prueba de la API

1. Ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```

2. Utiliza herramientas como curl, Postman o httpie para probar los endpoints de la API:

- GET /api/libros/ (Listar todos los libros)
- POST /api/libros/ (Crear un nuevo libro)
- GET /api/libros/<id>/ (Obtener un libro)
- PUT /api/libros/<id>/ (Actualizar un libro)
- DELETE /api/libros/<id>/ (Eliminar un libro)

---

- GET /api/categorias/ (Listar todos los libros)
- POST /api/categorias/ (Crear un nuevo libro)
- GET /api/categorias/<id>/ (Obtener un libro)
- PUT /api/categorias/<id>/ (Actualizar un libro)
- DELETE /api/categorias/<id>/ (Eliminar un libro)

---

Ejemplo usando curl:

```bash
# Listar todos los libros
curl http://localhost:8000/api/libros/

# Crear un nuevo libro
curl -X POST -H "Content-Type: application/json" -d '{"titulo":"Django para Principiantes","autor":"William S. Vincent","isbn":"9781735467207","fecha_publicacion":"2020-12-01"}' http://localhost:8000/api/libros/

# Obtener un libro (reemplaza <id> con un id real)
curl http://localhost:8000/api/libros/<id>/

# Actualizar un libro (reemplaza <id> con un id real)
curl -X PUT -H "Content-Type: application/json" -d '{"titulo":"Django para Profesionales","autor":"William S. Vincent","isbn":"9781735467214","fecha_publicacion":"2021-06-01"}' http://localhost:8000/api/libros/<id>/

# Eliminar un libro (reemplaza <id> con un id real)
curl -X DELETE http://localhost:8000/api/libros/<id>/
```

## Mejores Prácticas

1. Utiliza nombres significativos para tus modelos, vistas y URLs.
2. Implementa autenticación y permisos adecuados para tu API.
3. Utiliza viewsets y routers para APIs más complejas.
4. Implementa paginación para conjuntos de datos grandes.
5. Utiliza filtros y funcionalidad de búsqueda cuando sea apropiado.
6. Escribe pruebas para tus vistas y serializadores de API.
7. Documenta tu API utilizando herramientas como Swagger o ReDoc.

## Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/es/)
- [Documentación de Django REST Framework](https://www.django-rest-framework.org/)
- [Django para APIs (Libro de William S. Vincent)](https://djangoforapis.com/)
- [Classy Django REST Framework](https://www.cdrf.co/)
- [Django REST Framework: Relaciones de Serializador](https://www.django-rest-framework.org/api-guide/relations/)