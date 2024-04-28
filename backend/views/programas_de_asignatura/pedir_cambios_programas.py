from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer, CharField
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from django.core.exceptions import ValidationError

from backend.models import VersionProgramaAsignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR,
)
from backend.services import (
    ServicioRoles,
    ServicioVersionProgramaAsignatura,
    ServicioAuditoria,
)
from backend.common.choices import Roles, AccionesProgramaDeAsignatura


class PedirCambiosVersionProgramaAPI(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(Serializer):
        mensaje = CharField()

    def post(self, request, id_programa):
        usuario = request.user

        try:
            version_programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
                {"error": {"__all__": MENSAJE_ID_INEXISTENTE}},
                status=HTTP_400_BAD_REQUEST,
            )

        # Validar mje
        data = self.InputSerializer(data=request.data)
        if not data.is_valid():
            return Response({"error": data.errors}, status=HTTP_400_BAD_REQUEST)
        validated_data = data.validated_data
        mensaje = validated_data["mensaje"]

        servicio_roles = ServicioRoles()
        servicio_version_programa = ServicioVersionProgramaAsignatura()
        servicio_auditoria = ServicioAuditoria()

        roles = servicio_roles.obtener_roles_usuario(usuario)
        roles_directores = roles.filter(rol=Roles.DIRECTOR_CARRERA)

        if not roles_directores.exists():
            return Response(
                {"error": {"__all__": MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR}},
                status=HTTP_401_UNAUTHORIZED,
            )

        # TODO: PREGUNTA. Se que no ocurrira este caso peeeeero
        # Si un usuario tiene multiples roles de director para distintas carreras, una aprobacion deberia
        # contar para todos ono
        for rol in roles_directores:
            try:
                servicio_version_programa.pedir_cambios_programa_asignatura(
                    version_programa=version_programa, rol=rol, mensaje=mensaje
                )
                servicio_auditoria.auditar_revision(
                    request.user,
                    version_programa,
                    AccionesProgramaDeAsignatura.PEDIR_CAMBIOS,
                )
            except ValidationError as e:
                # La unica excepcion que tira es por no tener permisos
                return Response({"error": e.message_dict}, status=HTTP_401_UNAUTHORIZED)

        return Response()
