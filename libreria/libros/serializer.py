from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    categorias = serializers.SerializerMethodField()
    class Meta:
        model = Libro
        fields = '__all__'

    def get_categorias(self, obj):
        return [categoria.nombre_categoria for categoria in obj.categorias.all()]

    def create(self, validated_data):
        categorias_data = validated_data.pop('categorias', [])
        libro = Libro.objects.create(**validated_data)
        libro.categorias.set(categorias_data)
        return libro

    def update(self, instance, validated_data):
        categorias_data = validated_data.pop('categorias', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.categorias.set(categorias_data)
        return instance