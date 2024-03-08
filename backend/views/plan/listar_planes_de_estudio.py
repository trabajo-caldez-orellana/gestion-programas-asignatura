from rest_framework.serializers import Serializer, IntegerField, CharField
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.services import ServicioPlanDeEstudio

class APIListarPlanesDeEstudio(APIView):
    # permission_classes = [IsAuthenticated,]

    class OutputSerializer(Serializer):
        id = IntegerField()
        nombre = CharField()
        carrera_id = IntegerField()
        nombre_carrera = CharField(source="carrera.nombre")

    def get(self, request):
        servicio_planes = ServicioPlanDeEstudio()
        planes_de_estudio = servicio_planes.listar_todos_los_planes_activos()
        serializer_planes = self.OutputSerializer(planes_de_estudio, many=True)
        return Response({"data": serializer_planes.data})