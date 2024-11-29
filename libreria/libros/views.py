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
        data = request.data
        categoria_nombres = data.pop('categorias', [])
        categorias = Categoria.objects.filter(nombre_categoria__in=categoria_nombres)

        serializer = LibroSerializer(data=data)
        if serializer.is_valid():
            libro = serializer.create({
                **serializer.validated_data,
                'categorias': categorias
            })
            response_serializer = LibroSerializer(libro)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
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
            serializer = LibroSerializer(data=request.data)
            if serializer.is_valid():
                updated_libro = serializer.update(libro, serializer.validated_data)
                updated_serializer = LibroSerializer(updated_libro)
                return Response(updated_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            libro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
