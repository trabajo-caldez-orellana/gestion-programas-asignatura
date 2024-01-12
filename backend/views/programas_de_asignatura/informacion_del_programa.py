from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from backend.models import VersionProgramaAsignatura
from backend.services import ServicioRoles
from backend.common.choices import EstadoAsignatura, Roles
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
        Obtiene informacion de un programa
        """
        servicio_rol = ServicioRoles()

        roles = servicio_rol.obtener_roles_usuario(request.user)

        try:
            programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
                {"error": {"__all__": MENSAJE_ID_INEXISTENTE}},
                status=HTTP_400_BAD_REQUEST,
            )

        if programa.estado == EstadoAsignatura.APROBADO:
            data = serializer_programa_asignatura(programa)
            return Response({"data": data})

        tiene_permiso_de_ver_programa = False
        for rol in roles:
            if rol.rol == Roles.SECRETARIO:
                tiene_permiso_de_ver_programa = tiene_permiso_de_ver_programa | True

            if rol.rol == Roles.DIRECTOR_CARRERA:
                # Verifica que la carrera tenga esa asignatura!
                planes_relacionados = programa.asignatura.plan_de_estudio_set.all()
                planes = planes_relacionados.filter(carrera=rol.carrera)

                tiene_permiso_de_ver_programa = (
                    tiene_permiso_de_ver_programa | planes.exist()
                )

            else:
                tiene_permiso_de_ver_programa = tiene_permiso_de_ver_programa | (
                    rol.asignatura == programa.asignatura
                )

        if not tiene_permiso_de_ver_programa:
            return Response(
                {"error": {"__all__": MENSAJE_PERMISO_PROGRAMA}},
                status=HTTP_401_UNAUTHORIZED,
            )

        data = serializer_programa_asignatura(programa)
        return Response({"data": data})
