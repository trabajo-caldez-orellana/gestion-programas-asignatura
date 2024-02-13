from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404

from backend.services import obtener_programas_historial

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

        # Llamar al servicio para obtener los programas historiales
        data = obtener_programas_historial(carrera_id, semestre_id, asignatura_id, anio_lectivo_id)

        return Response(data)
