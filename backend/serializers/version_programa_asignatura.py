import json

from backend.common.choices import TipoDescriptor
from backend.models import (
    PlanDeEstudio,
    VersionProgramaAsignatura,
    Rol,
    ProgramaTieneActividadReservada,
    ProgramaTieneDescriptor,
)


def serialiar_datos_programa_asignatura(
    programa_de_asignatura: VersionProgramaAsignatura,
):
    asignatura = programa_de_asignatura.asignatura
    # Obtengo carreras en als cuales se dicta la asignatura
    planes_de_estudio = PlanDeEstudio.objects.filter(asignaturas__in=asignatura)
    carreras = []

    for plan in planes_de_estudio:
        carreras.append(plan.carrera)

    # Obtengo los docentes de la carrera
    docentes = []
    roles = Rol.objects.filter(asignatura=asignatura)
    for rol in roles:
        docentes.append(rol.usuario)

    # Obtengo los ejes transversales y descriptores
    descriptores_del_programa = ProgramaTieneDescriptor.objects.filter(
        version_programa_asignatura=programa_de_asignatura,
        descriptor__tipo=TipoDescriptor.DESCRIPTOR,
    )
    ejes_transversales_del_programa = ProgramaTieneDescriptor.objects.filter(
        version_programa_asignatura=programa_de_asignatura,
        descriptor__tipo=TipoDescriptor.EJE_TRANSVERSAL,
    )

    # Obtengo las actividades reservadas
    actividades_reservadas = ProgramaTieneActividadReservada.objects.filter(
        version_programa_asignatura=programa_de_asignatura
    )

    datos_programa = {
        "informacion_general": {
            "carreras": carreras,
            "docentes": docentes,
            "bloque_curricular": asignatura.bloque_curricular,
        },
        "carga_horaria": {
            "semanas_dictado": programa_de_asignatura.semanas_dictado,
            "semanal_teoria_presencial": programa_de_asignatura.semanal_teoria_presencial,
            "semanal_practica_presencial": programa_de_asignatura.semanal_practica_presencial,
            "semanal_lab_presencial": programa_de_asignatura.semanal_practica_presencial,
            "semanal_teorico_practico_presencial": programa_de_asignatura.semanal_teorico_practico_presencial,
            "semanal_teoria_remoto": programa_de_asignatura.semanal_teoria_remoto,
            "semanal_practica_remoto": programa_de_asignatura.semanal_practica_remoto,
            "semanal_lab_remoto": programa_de_asignatura.semanal_lab_remoto,
            "semanal_teorico_practico_remoto": programa_de_asignatura.semanal_teorico_practico_remoto,
        },
        "resultados_de_aprendizaje": json.loads(
            programa_de_asignatura.resultados_de_aprendizaje
        ),
        "ejes_transversales": ejes_transversales_del_programa,
        "actividades_reservadas": actividades_reservadas,
        "descriptores": descriptores_del_programa,
        "contenidos": programa_de_asignatura.contenidos,
        "bibliografia": programa_de_asignatura.bibliografia,
        "recursos": programa_de_asignatura.recursos,
        "evaluacion": programa_de_asignatura.evaluacion,
        "investigacion_docentes": programa_de_asignatura.investigacion_docentes,
        "investigacion_estudiantes": programa_de_asignatura.investigacion_estudiantes,
        "extension_docentes": programa_de_asignatura.extension_docentes,
        "extension_estudiantes": programa_de_asignatura.extension_estudiantes,
        "cronograma": programa_de_asignatura.cronograma,
    }

    return datos_programa
