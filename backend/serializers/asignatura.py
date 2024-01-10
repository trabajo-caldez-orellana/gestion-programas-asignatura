from rest_framework import serializers


class SerializerAsignatura(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
