from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.models import Carrera, Semestre, Asignatura, AnioAcademico


class ObtenerFiltros(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        carreras = Carrera.objects.all().order_by("nombre")
        semestres = Semestre.objects.all().order_by("fecha_inicio")
        asignaturas = Asignatura.objects.all().order_by("denominacion")
        anios_lectivos = AnioAcademico.objects.all().order_by("fecha_inicio")

        return Response(
            [
                {
                    "tipo": "carrera",
                    "nombre": "Carreras",
                    "opciones": [
                        {"id": carrera.id, "informacion": carrera.nombre}
                        for carrera in carreras
                    ],
                },
                {
                    "tipo": "semestre",
                    "nombre": "Semestres",
                    "opciones": [
                        {"id": semestre.id, "informacion": str(semestre)}
                        for semestre in semestres
                    ],
                },
                {
                    "tipo": "asignatura",
                    "nombre": "Asignaturas",
                    "opciones": [
                        {"id": asignatura.id, "informacion": asignatura.denominacion}
                        for asignatura in asignaturas
                    ],
                },
                {
                    "tipo": "anio_lectivo",
                    "nombre": "Años lectivos",
                    "opciones": [
                        {"id": anio.id, "informacion": str(anio)} for anio in anios_lectivos
                    ],
                },
            ]
        )
