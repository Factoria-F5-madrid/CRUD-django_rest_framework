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

## Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- Conocimientos básicos de Django y APIs RESTful

## Configuración del Proyecto

*Recuerda iniciar tu entorno virtual, sea que lo hagas con **"uv venv"** o con **"python -m venv venv"** por ejemplo, y actívalo*

1. Instala Django

```bash
pip install Django
```

2. Crea un nuevo proyecto Django:

```bash
django-admin startproject libreria
cd libreria
```

3. Crea dos aplicaciones:

```bash
python manage.py startapp libros
```
Y nuevamente:

```bash
python manage.py startapp categorias
```

4. Instala Django REST Framework:

```bash
pip install djangorestframework
```

5. Añade 'rest_framework' y 'libros' a INSTALLED_APPS en settings.py:

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
├── .env
├── app.py
```

## Conexión a la Base de Datos usando .env

Para proteger información sensible como las credenciales de tu base de datos, es recomendable usar un archivo `.env` para almacenar estas configuraciones de manera segura.

### Instalación de psycopg2 para usar postgreSQL

1. `psycopg2` es un paquete de Python que permite conectarte a bases de datos PostgreSQL desde tu código Python, de forma fácil y rápida.


```bash
 pip install psycopg2-binary
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

También puedes crear un archivo `.env.example` con la estructura que ves arriba.

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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Cambia el motor a postgres
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
from categorias.models import Categoria

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    fecha_publicacion = models.DateField()
    
    categorias = models.ManyToManyField(Categoria, related_name='categorias')

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
from categorias.models import Categoria

class LibroSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True
    )
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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Libro
from categorias.models import Categoria
from .serializer import LibroSerializer

class VistasLibros():
    @api_view(['GET'])
    def ListaLibros(request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def CrearLibros(request):

        serializer = LibroSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'PUT', 'DELETE'])
    def DetalleLibros(request, pk):
        try:
            libro = Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LibroSerializer(libro)
            return Response(serializer.data)

        elif request.method == 'PUT':
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
from .serializer import CategoriaSerializer

class VistasCategorias():
    @api_view(['GET'])
    def ListaCategorias(request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def crearCategorias(request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT', 'DELETE'])
    def DetalleCategorias(request, pk):
        try:
            categoria = Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CategoriaSerializer(categoria)
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
    path('', views.ListaLibros.as_view(), name='lista-libros'),
    path('<int:pk>', views.DetalleLibro.as_view(), name='detalle-libro'),
]
```

O también podría ser de esta manera:

```python
from django.urls import path
from .views import VistasLibros

urlpatterns = [
    path('', VistasLibros.ListaLibros, name="Lista_libros"),
    path('crear', VistasLibros.CrearLibros, name="crear_libros"),
    path('<int:pk>', VistasLibros.DetalleLibros, name="detalle_libros"),
]
```

Y luego en categorias/urls.py (crea este archivo si no existe):

```python
from django.urls import path
from .views import VistasCategorias

urlpatterns = [
    path('', VistasCategorias.ListaCategorias, name='lista-categoria'),
    path('crear', VistasCategorias.crearCategorias, name='crear-categoria'),
    path('<int:pk>', VistasCategorias.DetalleCategorias, name='detalle-categoria'),
]
```

2. En libreria/urls.py, incluye las URLs de la aplicación libros:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include([
            path('libros/', include('libros.urls')),
            path('categorias/', include('categorias.urls')),
    ])),
]

```
## Crea un front con Streamlit

1. Instala streamlit:

```plaintext
pip install streamlit
```

2. Crea un archivo llamado `app.py` e ingresa este código básico:

```python
import streamlit as st
import datetime
import requests

st.sidebar.title('Menú')
st.sidebar.write('Bienvenidxs a mi librería')

st.title('Bienvenidxs a mi librería')
st.write('Estos son mis libros desde mi API:')

# Mostrar libros existentes
response = requests.get('http://127.0.0.1:8000/v1/libros')
if response.status_code == 200:
    libros = response.json()
    for libro in libros:
        st.write(f"Titulo: {libro['titulo']}")
        st.write(f"Categorías: {', '.join([str(categoria) for categoria in libro['categorias']])}")
        if st.button(f"Ver detalle {libro['id']}"):
            st.write(libro)
        if st.button(f"Borrar {libro['id']}"):
            delete_response = requests.delete(f"http://127.0.0.1:8000/v1/libros/{libro['id']}")
            if delete_response.status_code == 204:
                st.write(f"Libro {libro['id']} borrado")
            else:
                st.write(f"No se pudo borrar el libro {libro['id']}")
else:
    st.write('No se encontraron libros')

# Obtener categorías existentes
categorias_response = requests.get('http://127.0.0.1:8000/v1/categorias')
categorias = []
if categorias_response.status_code == 200:
    categorias = categorias_response.json()

# Formulario para crear un nuevo libro
st.sidebar.title('Crear nuevo libro')
titulo = st.sidebar.text_input('Título')
autor = st.sidebar.text_input('Autor')
isbn = st.sidebar.text_input('ISBN')
fecha_publicacion = st.sidebar.date_input(
    'Fecha de publicación', 
    min_value=datetime.date(1, 1, 1),
    max_value=datetime.date.today()
)
categorias_seleccionadas = st.sidebar.multiselect(
    'Categorías', [categoria['id'] for categoria in categorias], format_func=lambda id: next(c['nombre_categoria'] for c in categorias if c['id'] == id)
)

if st.sidebar.button('Crear libro'):
    nuevo_libro = {
        'titulo': titulo,
        'autor': autor,
        'isbn': isbn,
        'fecha_publicacion': str(fecha_publicacion),
        'categorias': categorias_seleccionadas
    }
    create_response = requests.post('http://127.0.0.1:8000/v1/libros/crear', json=nuevo_libro)
    if create_response.status_code == 201:
        st.sidebar.write('Libro creado exitosamente')
    else:
        st.sidebar.write('Error al crear el libro!')
```

## Prueba de la API

1. Ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```
2. Ejecuta la aplicación de stremalit
```bash
streamlit run app.py
```

3. Utiliza herramientas como curl, Postman o httpie para probar los endpoints de la API:

- GET /v1/libros/ (Listar todos los libros)
- POST /v1/libros/crear/ (Crear un nuevo libro)
- GET /v1/libros/<id>/ (Obtener un libro)
- PUT /v1/libros/<id>/ (Actualizar un libro)
- DELETE /v1/libros/<id>/ (Eliminar un libro)

---

- GET /v1/categorias/ (Listar todos los categorias)
- POST /v1/categorias/crear/ (Crear un nuevo categoria)
- GET /v1/categorias/<id>/ (Obtener un categoria)
- PUT /v1/categorias/<id>/ (Actualizar un categoria)
- DELETE /v1/categorias/<id>/ (Eliminar un categoria)

---

### Hacer requests:

Crear Libro:

```json
{
    "titulo": "Libro test",
    "autor": "Autor 1",
    "isbn": "0000000000000000000",
    "fecha_publicacion": "1967-05-30",
    "categorias": [1, 8]
}

```

Modificar Libro:

```json
{
    "titulo": "Libro test",
    "autor": "Autor 2",
    "isbn": "0000000000000000000",
    "fecha_publicacion": "1967-06-30",
    "categorias": [1, 8]
}
```

Crear categoria:

```json
{
    "nombre_categoria": "Thriller"
}
```

Ejemplo usando curl:

```bash
# Listar todos los libros
curl http://localhost:8000/v1/libros/

# Crear un nuevo libro
curl -X POST -H "Content-Type: application/json" -d '{"titulo":"Django para Principiantes","autor":"William S. Vincent","isbn":"9781735467207","fecha_publicacion":"2020-12-01"}' http://localhost:8000/v1/libros/

# Obtener un libro (reemplaza <id> con un id real)
curl http://localhost:8000/v1/libros/<id>/

# Actualizar un libro (reemplaza <id> con un id real)
curl -X PUT -H "Content-Type: application/json" -d '{"titulo":"Django para Profesionales","autor":"William S. Vincent","isbn":"9781735467214","fecha_publicacion":"2021-06-01"}' http://localhost:8000/v1/libros/<id>/

# Eliminar un libro (reemplaza <id> con un id real)
curl -X DELETE http://localhost:8000/v1/libros/<id>/
```

## Mejores Prácticas

1. Utiliza nombres significativos para tus modelos, vistas y URLs.
2. Implementa autenticación y permisos adecuados para tu API.
3. Utiliza viewsets y routers para APIs más complejas.
4. Implementa paginación para conjuntos de datos grandes.
5. Utiliza filtros y funcionalidad de búsqueda cuando sea apropiado.
6. Escribe pruebas para tus vistas y serializadores de API.
7. Documenta tu API utilizando herramientas como Postman.

## Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/es/)
- [Documentación de Django REST Framework](https://www.django-rest-framework.org/)
- [Django para APIs (Libro de William S. Vincent)](https://djangoforapis.com/)
- [Classy Django REST Framework](https://www.cdrf.co/)
- [Django REST Framework: Relaciones de Serializador](https://www.django-rest-framework.org/api-guide/relations/)
- [Viewsets en django](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Rutas en Django](https://www.django-rest-framework.org/api-guide/routers/)
- [Migración de SQLite3 a MySQL](https://stackoverflow.com/questions/3034910/whats-the-best-way-to-migrate-a-django-db-from-sqlite-to-mysql)
