from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404

from backend.models import VersionProgramaAsignatura, PlanDeEstudio
from backend.common.choices import EstadoAsignatura
from backend.serializers import ProgramasVigentesSerializer


class ObtenerProgramasHistorial(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        Busca los programas
        """

        # Obtener parámetros de la URL
        carrera_id = request.query_params.get("carrera")
        semestre_id = request.query_params.get("semestre")
        asignatura_id = request.query_params.get("asignatura")
        anio_lectivo_id = request.query_params.get("anio_lectivo")

        # Verificar que todos los parámetros están presentes
        if not (carrera_id and semestre_id and asignatura_id and anio_lectivo_id):
            raise Http404("Faltan parámetros en la solicitud")

        # Convertir los IDs a enteros
        carrera_id = int(carrera_id)
        semestre_id = int(semestre_id)
        asignatura_id = int(asignatura_id)
        anio_lectivo_id = int(anio_lectivo_id)

        # Obtenemos los planes de estudio que contienen la carrera seleccionada
        planes_de_estudio = PlanDeEstudio.objects.filter(carrera_id=carrera_id)

        # Obtenemos las asignaturas relacionadas a los planes de estudio
        asignaturas_relacionadas = []

        for plan_de_estudio in planes_de_estudio:
            asignaturas_relacionadas.extend(plan_de_estudio.asignaturas.all())

        programas_historial = VersionProgramaAsignatura.objects.filter(
            asignatura__in=asignaturas_relacionadas,
            semestre_id=semestre_id,
            asignatura_id=asignatura_id,
            semestre__anio_academico_id=anio_lectivo_id,
            estado=EstadoAsignatura.APROBADO,
        )
        serializer = ProgramasVigentesSerializer()
        data = serializer.to_representation(programas_historial)

        return Response(data)
