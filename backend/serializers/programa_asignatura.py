import json
from rest_framework import serializers

from backend.models import (
    VersionProgramaAsignatura,
    ActividadReservada,
    Carrera,
    Estandar,
    ProgramaTieneActividadReservada,
    ProgramaTieneDescriptor,
    Rol,
    Correlativa
)
from backend.common.choices import TipoDescriptor, NivelDescriptor, Roles
from backend.serializers.asignatura import SerializerAsignaturaParaSeleccion

class SerializerProgramaTieneDescriptor(serializers.Serializer):
    id = serializers.IntegerField(source="descriptor_id")
    seleccionado = serializers.SerializerMethodField()
    nombre = serializers.CharField(source="descriptor__descripcion")

    def get_seleccionado(self, obj):
        return obj["nivel"] != NivelDescriptor.NADA


class SerializerProgramaTieneActividadReservada(serializers.Serializer):
    id = serializers.IntegerField(source="actividad_reservada_id")
    nivel = serializers.IntegerField()
    nombre = serializers.CharField(source="actividad_reservada__descripcion")


class SerializerProgramaTieneEjeTransversal(serializers.Serializer):
    id = serializers.IntegerField(source="descriptor_id")
    nivel = serializers.IntegerField()
    nombre = serializers.CharField(source="descriptor__descripcion")


class SerializerCorrelativa(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    tipo = serializers.CharField()
    requisito = serializers.CharField()
    asignatura = SerializerAsignaturaParaSeleccion(required=False, source="asignatura_correlativa", allow_null=True)
    modulo = serializers.CharField(required=False, allow_null=True)
    cantidadAsignaturas = serializers.CharField(required=False, source="cantidad_asignaturas", allow_null=True)

def serializer_programa_asignatura(
    programa: VersionProgramaAsignatura, solo_lectura: bool = False
):
    carreras_de_la_asignatura = Carrera.objects.filter(
        plandeestudio__asignaturas=programa.asignatura
    ).distinct()
    if not solo_lectura:
        # obtengo todos los estandares/programas a los que pertenece la asignatura
        carreras_id = [carrera.id for carrera in carreras_de_la_asignatura]
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
            for actividad in estandar.descriptores.filter(
                tipo=TipoDescriptor.EJE_TRANSVERSAL
            ):
                ejes_transversales_disponibles_para_modificar_programa.add(actividad)

        descriptores_del_programa = []
        ejes_transversales_del_programa = []
        actividades_reservadas_del_programa = []
        
        for descriptor in descriptores_disponibles_para_modificar_programa:
            try: 
                descriptor_del_programa = ProgramaTieneDescriptor.objects.get(
                    version_programa_asignatura_id=programa.id,
                    descriptor_id=descriptor.id
                )
                descriptores_del_programa.append(
                    {
                        "id": descriptor_del_programa.descriptor_id,
                        "nombre": descriptor_del_programa.descriptor.descripcion,
                        "seleccionado": descriptor_del_programa.nivel != NivelDescriptor.NADA
                    }
                )
            except ProgramaTieneDescriptor.DoesNotExist:
                descriptores_del_programa.append(
                    {
                        "id": descriptor.id,
                        "nombre": descriptor.descripcion,
                        "seleccionado": False
                    }
                )

        for eje in ejes_transversales_disponibles_para_modificar_programa:
            try: 
                eje_del_programa = ProgramaTieneDescriptor.objects.get(
                    version_programa_asignatura_id=programa.id,
                    descriptor_id=eje.id
                )
                ejes_transversales_del_programa.append(
                    {
                        "id": eje_del_programa.descriptor_id,
                        "nombre": eje_del_programa.descriptor.descripcion,
                        "nivel": eje_del_programa.nivel
                    }
                )
            except ProgramaTieneDescriptor.DoesNotExist:
                ejes_transversales_del_programa.append(
                    {
                        "id": eje.id,
                        "nombre": eje.descripcion,
                        "nivel": NivelDescriptor.NADA
                    }
                )
        
        for actividad in actividades_reservadas_disponibles_pera_modificar_programa:
            try: 
                actividad_del_programa = ProgramaTieneActividadReservada.objects.get(
                    version_programa_asignatura_id=programa.id,
                    actividad_reservada_id=actividad.id
                )
                actividades_reservadas_del_programa.append(
                    {
                        "id": actividad_del_programa.actividad_reservada_id,
                        "nombre": actividad_del_programa.actividad_reservada.descripcion,
                        "nivel": actividad_del_programa.nivel
                    }
                )
            except ProgramaTieneActividadReservada.DoesNotExist:
                actividades_reservadas_del_programa.append(
                    {
                        "id": actividad.id,
                        "nombre": actividad.descripcion,
                        "nivel": NivelDescriptor.NADA
                    }
                )

    else:
        # El array con el nivel
        descriptores_del_programa = ProgramaTieneDescriptor.objects.filter(
            version_programa_asignatura=programa, descriptor__tipo=TipoDescriptor.DESCRIPTOR
        ).values("descriptor_id", "descriptor__descripcion", "nivel")
        ejes_transversales_del_programa = ProgramaTieneDescriptor.objects.filter(
            version_programa_asignatura=programa,
            descriptor__tipo=TipoDescriptor.EJE_TRANSVERSAL,
        ).values("descriptor_id", "descriptor__descripcion", "nivel")
        actividades_reservadas_del_programa = (
            ProgramaTieneActividadReservada.objects.filter(
                version_programa_asignatura=programa
            )
        ).values("actividad_reservada_id", "actividad_reservada__descripcion", "nivel")

        descriptores_del_programa = SerializerProgramaTieneDescriptor(
            descriptores_del_programa, many=True
        ).data
        ejes_transversales_del_programa = SerializerProgramaTieneEjeTransversal(
            ejes_transversales_del_programa, many=True
        ).data
        actividades_reservadas_del_programa = SerializerProgramaTieneActividadReservada(
            actividades_reservadas_del_programa, many=True
        ).data

    equipo_docente = Rol.objects.filter(
        rol__in=[Roles.TITULAR_CATEDRA, Roles.DOCENTE],
        asignatura_id=programa.asignatura.id
    )

    equipo_docente_inforamacion = [
        {
            "id": rol.id,
            "informacion": f"{str(rol.usuario)} - {rol.get_rol()} - {rol.get_dedicacion()}"
        }
        for rol in equipo_docente
    ]

    correlativas_programa = Correlativa.objects.filter(version_programa_asignatura_id=programa.id)
    serializador_correlativas = SerializerCorrelativa(correlativas_programa, many=True)

    return {
        "id": programa.id,
        "informacion_general": {
            "nombre_asignatura": programa.asignatura.denominacion,
            "codigo_aignatura": programa.asignatura.codigo,
            "anio_academico": str(programa.semestre.anio_academico),
            "bloque_curricular": programa.asignatura.bloque_curricular.nombre,
            "carreras": [{"id": carrera.id, "informacion": carrera.nombre} for carrera in carreras_de_la_asignatura],
            "equipo_docente": equipo_docente_inforamacion,
        },
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
            "fundamentacion": programa.fundamentacion,
            "contenidos": programa.contenidos,
            "bibliografia": programa.bibliografia,
            "metodologia_aplicada": programa.metodologia_aplicada,
            "recursos": programa.recursos,
            "cronograma": programa.cronograma,
            "evaluacion": programa.evaluacion,
            "investigacion_docentes": programa.investigacion_docentes,
            "investigacion_estudiantes": programa.investigacion_estudiantes,
            "extension_docentes": programa.extension_docentes,
            "extension_estudiantes": programa.extension_estudiantes,
        },
        "correlativas": serializador_correlativas.data
    }
