from rest_framework import serializers

from backend.models import (
    VersionProgramaAsignatura,
    ActividadReservada,
    Carrera,
    Estandar,
    ProgramaTieneActividadReservada,
    ProgramaTieneDescriptor,
)
from backend.common.choices import TipoDescriptor


class SerializerProgramaTieneDescriptor(serializers.Serializer):
    id = serializers.IntegerField(source="descriptor_id")
    nivel = serializers.IntegerField()
    nombre = serializers.CharField(source="descriptor__descripcion")


class SerializerProgramaTieneActividadReservada(serializers.Serializer):
    id = serializers.IntegerField(source="actividad_reservada_id")
    nivel = serializers.IntegerField()
    nombre = serializers.CharField(source="actividad_reservada__descripcion")


# TODO. Modificar para que sea solo lectura
def serializer_programa_asignatura(
    programa: VersionProgramaAsignatura, solo_lectura: bool = False
):
    if not solo_lectura:
        # obtengo todos los estandares/programas a los que pertenece la asignatura
        carreras = Carrera.objects.filter(
            plandeestudio__asignaturas=programa.asignatura
        ).distinct()
        carreras_id = [carrera.id for carrera in carreras]
        # obtengo todos los estandares relacionadas a la carrera
        estandares = Estandar.objects.filter(carrera_id__in=carreras_id)
        estandares_id = [estandar.id for estandar in estandares]

        # Obtengo las actividades reservadas
        actividades_reservadas_disponibles_pera_modificar_programa = (
            ActividadReservada.objects.filter(estandar_id__in=estandares_id)
        )

        # obtengo todos los descriptores posibles
        descriptores_disponibles_para_modificar_programa = set()
        ejes_transversales_disponibles_para_modificar_programa = set()
        for estandar in estandares:
            for descriptor in estandar.descriptores.filter(
                tipo=TipoDescriptor.DESCRIPTOR
            ):
                descriptores_disponibles_para_modificar_programa.add(descriptor)
            for eje in estandar.descriptores.filter(
                tipo=TipoDescriptor.EJE_TRANSVERSAL
            ):
                ejes_transversales_disponibles_para_modificar_programa.add(eje)

    # El array con el nivel
    descriptores_del_programa = ProgramaTieneDescriptor.objects.filter(
        version_programa_asignatura=programa
    ).values("descriptor_id", "descriptor__descripcion", "nivel")
    ejes_transversales_del_programa = ProgramaTieneDescriptor.objects.filter(
        version_programa_asignatura=programa
    ).values("descriptor_id", "descriptor__descripcion", "nivel")
    actividades_reservadas_del_programa = (
        ProgramaTieneActividadReservada.objects.filter(
            version_programa_asignatura=programa
        )
    ).values("actividad_reservada_id", "actividad_reservada__descripcion", "nivel")

    if solo_lectura:
        descriptores_del_programa = SerializerProgramaTieneDescriptor(
            descriptores_del_programa, many=True
        ).data
        ejes_transversales_del_programa = SerializerProgramaTieneDescriptor(
            ejes_transversales_del_programa, many=True
        ).data
        actividades_reservadas_del_programa = SerializerProgramaTieneActividadReservada(
            actividades_reservadas_del_programa, many=True
        ).data
    else:
        # TODO: controlar que descriptores estan asociados con el programa y cuales no, y
        # Armar un array con el formato necesario
        descriptores_del_programa = []
        ejes_transversales_del_programa = []
        descriptores_del_programa = []

    return {
        "id": programa.id,
        "carga_horaria": {
            "semanas_dictado": programa.asignatura.semanas_dictado,
            "teoria_presencial": programa.asignatura.semanal_teoria_presencial,
            "practica_presencial": programa.asignatura.semanal_practica_presencial,
            "teorico_practico_presencial": programa.asignatura.semanal_teorico_practico_presencial,
            "laboratorio_presencial": programa.asignatura.semanal_lab_presencial,
            "teoria_distancia": programa.asignatura.semanal_teoria_remoto,
            "practica_distancia": programa.asignatura.semanal_practica_remoto,
            "teorico_practico_distancia": programa.asignatura.semanal_teorico_practico_remoto,
            "laboratorio_distancia": programa.asignatura.semanal_lab_remoto,
        },
        "descriptores": {
            "resultados_de_aprendizaje": programa.resultados_de_aprendizaje,
            "ejes_transversales": ejes_transversales_del_programa,
            "descriptores": descriptores_del_programa,
            "actividades_reservadas": actividades_reservadas_del_programa,
        },
        "informacion_adicional": {
            "fundamentacion": "",
            "contenidos": programa.contenidos,
            "bibliografia": programa.bibliografia,
            "metodologia_aplicada": "",
            "recursos": programa.recursos,
            "evaluacion": programa.evaluacion,
            "investigacion_docentes": programa.investigacion_docentes,
            "investigacion_estudiantes": programa.investigacion_estudiantes,
            "extension_docentes": programa.extension_docentes,
            "extension_estudiantes": programa.extension_estudiantes,
        },
    }
