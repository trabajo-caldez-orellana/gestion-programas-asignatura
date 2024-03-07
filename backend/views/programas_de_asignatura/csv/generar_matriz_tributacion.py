
import csv
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.http import HttpResponse
from django.core.exceptions import ValidationError

from backend.models import Carrera, PlanDeEstudio
from backend.services.obtener_datos_matriz import ObtenerDatosMatriz
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_CARRERA_PLAN,
)



class GenerarMatriz(APIView):
    # permission_classes = [
    #     IsAuthenticated,
    # ]

    def get(self, request, id_carrera, id_plan_de_estudio):
        try:
            carrera = Carrera.objects.get(id=id_carrera)
        except Carrera.DoesNotExist:
            return Response({"error": {"carrera": MENSAJE_ID_INEXISTENTE}}, status=HTTP_400_BAD_REQUEST)
        
        try:
            plan_de_estudio = PlanDeEstudio.objects.get(id=id_plan_de_estudio)
        except PlanDeEstudio.DoesNotExist:
            return Response({"error": {"plan_de_estudio": MENSAJE_ID_INEXISTENTE}}, status=HTTP_400_BAD_REQUEST)

        # Verifico que el plan de estudio pertenezca a la carrera
        if carrera.id != plan_de_estudio.carrera_id:
            return Response({"error": {"__all__": MENSAJE_CARRERA_PLAN}}, status=HTTP_400_BAD_REQUEST)
            

        obtener_datos_matriz = ObtenerDatosMatriz()
        try:
          datos_matriz = obtener_datos_matriz.obtener_datos_matriz_de_tributacion(carrera, plan_de_estudio)
        except ValidationError as e:
            return Response({"error": e.message_dict}, status=HTTP_400_BAD_REQUEST)

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="matriz-tributacion.csv"'},
        )

        writer = csv.writer(response)
        for fila in datos_matriz:
            writer.writerow(fila)

        return response