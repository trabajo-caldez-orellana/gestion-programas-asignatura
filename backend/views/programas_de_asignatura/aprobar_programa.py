from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from django.core.exceptions import ValidationError

from backend.models import VersionProgramaAsignatura
from backend.common.mensajes_de_error import MENSAJE_ID_INEXISTENTE, MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR
from backend.services import ServicioRoles, ServicioVersionProgramaAsignatura
from backend.common.choices import Roles 

class AprobarVersionProgramaAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id_programa):
        usuario = request.user

        try:
            version_programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response({"error": {"__all__": MENSAJE_ID_INEXISTENTE}}, status=HTTP_400_BAD_REQUEST)
        
        servicio_roles = ServicioRoles()
        servicio_version_programa = ServicioVersionProgramaAsignatura()

        roles = servicio_roles.obtener_roles_usuario(usuario)
        roles_directores = roles.filter(rol=Roles.DIRECTOR_CARRERA)

        if not roles_directores.exists():
            return Response({"error": {"__all__": MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR}}, status=HTTP_401_UNAUTHORIZED)
        
        # PREGUNTA. Se que no ocurrira este caso peeeeero
        # Si un usuario tiene multiples roles de director para distintas carreras, una aprobacion deberia
        # contar para todos ono
        for rol in roles_directores:
            try:
              servicio_version_programa.aprobar_programa_de_asignatura(
                  version_programa=version_programa,
                  rol=rol
              )
            except ValidationError as e:
              # La unica excepcion que tira es por no tener permisos
              return Response({"error": e.message_dict}, status=HTTP_401_UNAUTHORIZED)
                

        return Response()

