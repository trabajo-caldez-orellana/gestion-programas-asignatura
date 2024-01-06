from rest_framework.views import APIView
from rest_framework.response import Response

from backend.models import Carrera, Semestre, Asignatura, AnioAcademico


class ObtenerFiltrosHistorial(APIView):
    def get(self, request):
        carreras = Carrera.objects.all().order_by("nombre")
        semestres = Semestre.objects.all().order_by("fecha_inicio")
        asignaturas = Asignatura.objects.all().order_by("denominacion")
        anios_lectivos = AnioAcademico.objects.all().order_by("fecha_inicio")

        return Response(
            {
                "data": {
                    "carreras": [
                        {"id": carrera.id, "nombre": carrera.nombre}
                        for carrera in carreras
                    ],
                    "semestres": [
                        {"id": semestre.id, "nombre": str(semestre)}
                        for semestre in semestres
                    ],
                    "asignaturas": [
                        {"id": asignatura.id, "nombre": asignatura.denominacion}
                        for asignatura in asignaturas
                    ],
                    "anios_lectivos": [
                        {"id": anio.id, "nombre": str(anio)} for anio in anios_lectivos
                    ],
                }
            }
        )
