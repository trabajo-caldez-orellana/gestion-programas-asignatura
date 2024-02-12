from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from backend.models import VersionProgramaAsignatura
from backend.common.choices import EstadoAsignatura
from backend.services import ServicioRoles
from backend.serializers import serializer_programa_asignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
    MENSAJE_PROGRAMA_APROBADO,
)


class InformacionModificacionProgramaAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_programa):
        """
        Obtiene informacion necesaria para el formulario de modificacion de un determinado programa.
        Devuelve las opciones posibles de ejes transversales, actividades reservadas, descriptores, etc.
        """
        servicio_rol = ServicioRoles()
        try:
            programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
                {"error": MENSAJE_ID_INEXISTENTE},
                status=HTTP_400_BAD_REQUEST,
            )

        if programa.estado == EstadoAsignatura.APROBADO:
            return Response(
                {
                    "error": MENSAJE_PROGRAMA_APROBADO,
                },
                status=HTTP_400_BAD_REQUEST,
            )

        if servicio_rol.usuario_tiene_permiso_para_acceder_a_programa(
            usuario=request.user, programa=programa
        ):
            # Obtiene los datos del programa, con informacion extra para su modificacion
            data = serializer_programa_asignatura(programa)
            return Response({"data": data})

        return Response(
            {"error": MENSAJE_PERMISO_PROGRAMA},
            status=HTTP_401_UNAUTHORIZED,
        )
