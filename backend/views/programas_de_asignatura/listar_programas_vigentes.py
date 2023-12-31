from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.models import VersionProgramaAsignatura
from backend.services import ServicioSemestre
from backend.common.choices import EstadoAsignatura
from backend.serializers import ProgramasVigentesSerializer

class ListarProgramasVigentesAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        Lista los programas vigentes
        """

        servicio_semestre = ServicioSemestre()

        semestre_actual = servicio_semestre.obtener_semestre_actual()

        programas_vigentes = VersionProgramaAsignatura.objects.filter(
            semestre = semestre_actual, estado = EstadoAsignatura.APROBADO
        )

        serializer = ProgramasVigentesSerializer()
        data = serializer.to_representation(programas_vigentes)

        return Response(data)
