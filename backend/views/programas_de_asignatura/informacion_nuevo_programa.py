from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from backend.models import Asignatura
from backend.services import ServicioRoles, ServicioVersionProgramaAsignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
)


class InformacionNuevoProgramaAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_asignatura):
        """
        Obtiene informacion de un programa, modo solo lectura
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

        if servicio_rol.usuario_tiene_permiso_para_crear_programa(
            usuario=request.user, asignatura=asignatura
        ):
            # TODO: obtener datos para crear un programa
            data = servicio_programa.obtener_datos_para_nuevo_programa(asignatura)
            return Response({"data": data})

        return Response(
            {"error": MENSAJE_PERMISO_PROGRAMA},
            status=HTTP_401_UNAUTHORIZED,
        )
