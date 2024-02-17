from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework import serializers

from django.core.exceptions import ValidationError

from backend.models import Asignatura
from backend.serializers import serializer_programa_asignatura
from backend.services import ServicioRoles, ServicioVersionProgramaAsignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
)


class SerializerDescriptor(serializers.Serializer):
    seleccionado = serializers.BooleanField()
    id = serializers.CharField()

class SerializadorEjesyActividades(serializers.Serializer):
    nivel = serializers.IntegerField()
    id = serializers.CharField()

class NuevoProgramaAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]


    class InputSerializer(serializers.Serializer):
        resultados_de_aprendizaje = serializers.JSONField()
        contenidos = serializers.CharField()
        bibliografia = serializers.CharField()
        recursos = serializers.CharField()
        evaluacion = serializers.CharField()
        investigacion_docentes = serializers.CharField()
        investigacion_estudiantes = serializers.CharField()
        extension_docentes = serializers.CharField()
        extension_estudiantes = serializers.CharField()
        cronograma = serializers.CharField()
        metodologia_aplicada = serializers.CharField()
        fundamentacion= serializers.CharField()

        # TODO. Verificar si es la manera correcta de hacerlo
        descriptores = SerializerDescriptor(many=True)
        actividades_reservadas = SerializadorEjesyActividades(many=True)
        ejes_transversales = SerializadorEjesyActividades(many=True)
        presentar_a_aprobacion = serializers.BooleanField()
        

    def post(self, request, id_asignatura):
        """Crea un nuevo programa
        """
        servicio_rol = ServicioRoles()
        servicio_programa = ServicioVersionProgramaAsignatura()

        try:
            asignatura = Asignatura.objects.get(id=id_asignatura)
        except Asignatura.DoesNotExist:
            return Response(
                {"error": MENSAJE_ID_INEXISTENTE},
                status=HTTP_400_BAD_REQUEST,
            )

        if not servicio_rol.usuario_tiene_permiso_para_crear_programa(
            usuario=request.user, asignatura=asignatura
        ):
            return Response(
                {"error": MENSAJE_PERMISO_PROGRAMA},
                status=HTTP_401_UNAUTHORIZED,
            )
        
        data = self.InputSerializer(data=request.data)
        if not data.is_valid():
            return Response({"error": data.errors}, status=HTTP_400_BAD_REQUEST)
        validated_data = data.validated_data
        try:
            programa_modificado = servicio_programa.crear_nueva_version_programa_asignatura(
                asignatura=asignatura,
                descriptores=validated_data["descriptores"],
                actividades_reservadas=validated_data["actividades_reservadas"],
                ejes_transversales=validated_data["ejes_transversales"],
                contenidos=validated_data["contenidos"],
                cronograma=validated_data["cronograma"],
                resultados_de_aprendizaje=validated_data["resultados_de_aprendizaje"],
                bibliografia=validated_data["bibliografia"],
                recursos=validated_data["recursos"],
                evaluacion=validated_data["evaluacion"],
                investigacion_docentes=validated_data["investigacion_docentes"],
                investigacion_estudiantes=validated_data["investigacion_estudiantes"],
                extension_docentes=validated_data["extension_docentes"],
                extension_estudiantes=validated_data["extension_estudiantes"],
                metodologia_aplicada = validated_data["metodologia_aplicada"],
                fundamentacion = validated_data["fundamentacion"],
            )
        except ValidationError as e:
            return Response({"error": e.message_dict}, status=HTTP_400_BAD_REQUEST)


        if validated_data["presentar_a_aprobacion"]:
            try:
                servicio_programa.presentar_programa_para_aprobacion(programa_modificado)
            except ValidationError as e:
                return Response({"error": e.message_dict}, status=HTTP_400_BAD_REQUEST)

        return Response({"data": serializer_programa_asignatura(programa_modificado, solo_lectura=True)})
