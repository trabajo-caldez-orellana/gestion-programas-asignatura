from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        carrera_id = request.query_params.get("carrera", None)
        semestre_id = request.query_params.get("semestre", None)
        asignatura_id = request.query_params.get("asignatura", None)
        anio_lectivo_id = request.query_params.get("anio_lectivo", None)

        # Convertir los IDs a enteros
        if carrera_id is not None:
            carrera_id = int(carrera_id)

        if semestre_id is not None:
            semestre_id = int(semestre_id)

        if asignatura_id is not None:
            asignatura_id = int(asignatura_id)

        if anio_lectivo_id is not None:
            anio_lectivo_id = int(anio_lectivo_id)

        # Llamar al servicio para obtener los programas historiales
        data = obtener_programas_historial(
            carrera_id, semestre_id, asignatura_id, anio_lectivo_id
        )

        return Response(data)
