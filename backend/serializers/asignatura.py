from rest_framework import serializers


class SerializerAsignatura(serializers.Serializer):
    id = serializers.IntegerField()
    denominacion = serializers.CharField()

class SerializerAsignaturaParaSeleccion(serializers.Serializer):
    id = serializers.IntegerField()
    informacion = serializers.CharField(source="denominacion")