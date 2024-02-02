from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from backend.models import VersionProgramaAsignatura
from backend.services import ServicioRoles
from backend.serializers import serializer_programa_asignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
)


class InformacionProgramaAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_programa):
        """
        Obtiene informacion de un programa, modo solo lectura
        """
        servicio_rol = ServicioRoles()
        try:
            programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
                {"error": MENSAJE_ID_INEXISTENTE},
                status=HTTP_400_BAD_REQUEST,
            )

        if servicio_rol.usuario_tiene_permiso_para_acceder_a_programa(
            usuario=request.user, programa=programa
        ):
            data = serializer_programa_asignatura(programa, True)
            return Response({"data": data})

        return Response(
            {"error": MENSAJE_PERMISO_PROGRAMA},
            status=HTTP_401_UNAUTHORIZED,
        )
