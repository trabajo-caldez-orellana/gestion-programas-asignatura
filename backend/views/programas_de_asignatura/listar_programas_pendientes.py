from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from django.core.exceptions import ValidationError

from backend.services import ServicioRoles, ServicioVersionProgramaAsignatura
from backend.common.mensajes_de_error import MENSAJE_PERMISO_PROGRAMAS_PENDIENTES


class ListarProgramasPendientesAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        Lista los programas
        """
        servicio_rol = ServicioRoles()
        servicio_versiones_programa = ServicioVersionProgramaAsignatura()

        roles = servicio_rol.obtener_roles_usuario(request.user)
        if not roles.exists():
            return Response(
                {"detail": MENSAJE_PERMISO_PROGRAMAS_PENDIENTES},
                status=HTTP_401_UNAUTHORIZED,
            )
        try:
            pendientes = servicio_versiones_programa.listar_tareas_pendientes_roles(
                roles
            )
        except ValidationError as e:
            return Response({"error": e.message_dict}, status=HTTP_400_BAD_REQUEST)

        return Response({"data": pendientes})
