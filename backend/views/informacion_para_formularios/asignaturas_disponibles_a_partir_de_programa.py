from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from backend.common.mensajes_de_error import MENSAJE_ID_INEXISTENTE
from backend.models import VersionProgramaAsignatura
from backend.services import ServicioPlanDeEstudio
from backend.serializers import SerializerAsignaturaParaSeleccion

class AsignaturasDisponiblesAPartirPrograma(APIView):
    def get(self, request, id_programa):
        try:
            programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
              status=HTTP_400_BAD_REQUEST,
              data={"error": {"__all__": MENSAJE_ID_INEXISTENTE}}
            )
        
        servicio_planes = ServicioPlanDeEstudio()
        listado_asignaturas = servicio_planes.obtener_asignaturas_disponibles_para_correlativa(
            programa.asignatura
        )

        serializer_asignatura = SerializerAsignaturaParaSeleccion(
            listado_asignaturas, many=True
        )
        return Response({"data": serializer_asignatura.data})