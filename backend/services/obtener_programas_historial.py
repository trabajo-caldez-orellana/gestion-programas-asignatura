from django.db.models import Q

from backend.models import PlanDeEstudio, VersionProgramaAsignatura
from backend.common.choices import EstadoAsignatura
from backend.serializers import ProgramasVigentesSerializer


def obtener_programas_historial(
    carrera_id, semestre_id, asignatura_id, anio_lectivo_id
):
    # Obtenemos los planes de estudio que contienen la carrera seleccionada
    filtros = Q()

    if carrera_id is not None:
        planes_de_estudio = PlanDeEstudio.objects.filter(carrera_id=carrera_id)

        # Obtenemos las asignaturas relacionadas a los planes de estudio
        asignaturas_relacionadas = []
        for plan_de_estudio in planes_de_estudio:
            asignaturas_relacionadas.extend(plan_de_estudio.asignaturas.all())
        asignaturas_relacionadas = set(asignaturas_relacionadas)
        id_asignaturas_relacionadas = [
            asignatura.id for asignatura in asignaturas_relacionadas
        ]
        filtros &= Q(asignatura_id__in=id_asignaturas_relacionadas)

    if semestre_id is not None:
        filtros &= Q(semestre_id=semestre_id)

    if asignatura_id is not None:
        filtros &= Q(asignatura_id=asignatura_id)

    if anio_lectivo_id is not None:
        filtros &= Q(semestre__anio_academico_id=anio_lectivo_id)

    filtros &= Q(estado=EstadoAsignatura.APROBADO)

    programas_historial = VersionProgramaAsignatura.objects.filter(filtros)
    serializer = ProgramasVigentesSerializer()
    data = serializer.to_representation(programas_historial)
    return data
