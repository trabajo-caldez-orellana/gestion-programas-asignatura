from backend.models import PlanDeEstudio, VersionProgramaAsignatura
from backend.common.choices import EstadoAsignatura
from backend.serializers import ProgramasVigentesSerializer

def obtener_programas_historial(carrera_id, semestre_id, asignatura_id, anio_lectivo_id):
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
    
    return data
