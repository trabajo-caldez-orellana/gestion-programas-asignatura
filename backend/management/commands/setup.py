from django.db import transaction
from django.core.management import BaseCommand

from backend.common.choices import (
    Semestres,
    MetodologiaAsignatura,
    TipoDescriptor
)
from backend.common.funciones_fecha import (
    obtener_fecha_actual,
    crear_fecha
)
from backend.models import (
    Carrera,
    PlanDeEstudio,
    Estandar,
    Descriptor,
    ActividadReservada,
    Asignatura,
    AnioAcademico,
    Semestre,
    BloqueCurricular
)

NOMBRES_CARRERAS = [
    "Ingeniería en Computación",
    "Ingeniería Química",
    "Ingeniería Informática",
]

NOMBRES_BLOQUES_CURRICULARES = [
    "Ciencias Básicas",
    "Tecnologías Básicas",
    "Tecnologías Aplicadas",
    "Complementarias"
]

INFORMACION_ASIGNATURAS_COMPARTIDAS = [
    {
      "denominacion": "Cálculo I",
      "codigo": "15_CCI",
      "metodologia": MetodologiaAsignatura.HIBRIDO,
      "semanas_dictado": 16,
      "semanal_teoria_presencial": 2,
      "semanal_practica_presencial": 2,
      "semanal_teorico_practico_presencial": 0,
      "semanal_lab_presencial": 0,
      "semanal_teoria_remoto": 0,
      "semanal_practica_remoto": 0,
      "semanal_teorico_practico_remoto": 2,
      "semanal_lab_remoto": 0,
      "horas_evaluacion": 2,
      "carga_rtf": 12,
      "semestre_dictado": Semestres.PRIMER
    },
    {
      "denominacion": "Cálculo II",
      "codigo": "15_CII",
      "metodologia": MetodologiaAsignatura.PRESENCIAL,
      "semanas_dictado": 16,
      "semanal_teoria_presencial": 2,
      "semanal_practica_presencial": 2,
      "semanal_teorico_practico_presencial": 2,
      "semanal_lab_presencial": 0,
      "semanal_teoria_remoto": None,
      "semanal_practica_remoto": None,
      "semanal_teorico_practico_remoto": None,
      "semanal_lab_remoto": None,
      "horas_evaluacion": 2,
      "carga_rtf": 12,
      "semestre_dictado": Semestres.SEGUNDO
    },
    {
      "denominacion": "Cálculo III",
      "codigo": "15_CAL",
      "metodologia": MetodologiaAsignatura.VIRTUAL,
      "semanas_dictado": 16,
      "semanal_teoria_presencial": None,
      "semanal_practica_presencial": None,
      "semanal_teorico_practico_presencial": None,
      "semanal_lab_presencial": None,
      "semanal_teoria_remoto": 2,
      "semanal_practica_remoto": 2,
      "semanal_teorico_practico_remoto": 2,
      "semanal_lab_remoto": 0,
      "horas_evaluacion": 2,
      "carga_rtf": 12,
      "semestre_dictado": None
    }
]


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        # Crear los tres anios lectivos con sus respectivos cuatrimestres
        anio_actual = obtener_fecha_actual().year
        # Anio lectivo anterior
        fecha_inicio_anio_anterior = crear_fecha(anio_actual-1, 1, 1)
        fecha_fin_anio_anterior = crear_fecha(anio_actual-1, 12, 31)
        fecha_cambio_cuatrimestre_anio_anterior = crear_fecha(anio_actual-1, 6, 30)
        fecha_cambio_cuatrimestre_anio_anterior_2 = crear_fecha(anio_actual-1, 7, 1)
        anio_lectivo_anterior = AnioAcademico(
            fecha_inicio=fecha_inicio_anio_anterior,
            fecha_fin=fecha_fin_anio_anterior
        )
        anio_lectivo_anterior.full_clean()
        anio_lectivo_anterior.save()

        primer_semestre_anio_anterior = Semestre(
            fecha_inicio=fecha_inicio_anio_anterior,
            fecha_fin=fecha_cambio_cuatrimestre_anio_anterior,
            anio_academico=anio_lectivo_anterior,
            semestre=Semestres.PRIMER
        )
        primer_semestre_anio_anterior.full_clean()
        primer_semestre_anio_anterior.save()
        segundo_semestre_anio_anterior = Semestre(
            fecha_inicio=fecha_cambio_cuatrimestre_anio_anterior_2,
            fecha_fin=fecha_fin_anio_anterior,
            anio_academico=anio_lectivo_anterior,
            semestre=Semestres.SEGUNDO
        )
        segundo_semestre_anio_anterior.full_clean()
        segundo_semestre_anio_anterior.save()


        # Anio lectivo actual
        fecha_inicio_anio_actual = crear_fecha(anio_actual, 1, 1)
        fecha_fin_anio_actual = crear_fecha(anio_actual, 12, 31)
        fecha_cambio_cuatrimestre_anio_actual = crear_fecha(anio_actual, 6, 30)
        fecha_cambio_cuatrimestre_anio_actual_2 = crear_fecha(anio_actual, 7, 1)
        anio_lectivo_actual = AnioAcademico(
            fecha_inicio=fecha_inicio_anio_actual,
            fecha_fin=fecha_fin_anio_actual
        )
        anio_lectivo_actual.full_clean()
        anio_lectivo_actual.save()

        primer_semestre_anio_actual = Semestre(
            fecha_inicio=fecha_inicio_anio_actual,
            fecha_fin=fecha_cambio_cuatrimestre_anio_actual,
            anio_academico=anio_lectivo_actual,
            semestre=Semestres.PRIMER
        )
        primer_semestre_anio_actual.full_clean()
        primer_semestre_anio_actual.save()
        segundo_semestre_anio_actual = Semestre(
            fecha_inicio=fecha_cambio_cuatrimestre_anio_actual_2,
            fecha_fin=fecha_fin_anio_actual,
            anio_academico=anio_lectivo_actual,
            semestre=Semestres.SEGUNDO
        )
        segundo_semestre_anio_actual.full_clean()
        segundo_semestre_anio_actual.save()



        # Anio lectivo siguiente
        fecha_inicio_anio_siguiente = crear_fecha(anio_actual + 1, 1, 1)
        fecha_fin_anio_siguiente = crear_fecha(anio_actual + 1, 12, 31)
        fecha_cambio_cuatrimestre_anio_siguiente = crear_fecha(anio_actual + 1, 6, 30)
        fecha_cambio_cuatrimestre_anio_siguiente_2 = crear_fecha(anio_actual + 1, 7, 1)
        anio_lectivo_siguiente = AnioAcademico(
            fecha_inicio=fecha_inicio_anio_siguiente,
            fecha_fin=fecha_fin_anio_siguiente
        )
        anio_lectivo_siguiente.full_clean()
        anio_lectivo_siguiente.save()

        primer_semestre_anio_siguiente = Semestre(
            fecha_inicio=fecha_inicio_anio_siguiente,
            fecha_fin=fecha_cambio_cuatrimestre_anio_siguiente,
            anio_academico=anio_lectivo_siguiente,
            semestre=Semestres.PRIMER
        )
        primer_semestre_anio_siguiente.full_clean()
        primer_semestre_anio_siguiente.save()
        segundo_semestre_anio_siguiente = Semestre(
            fecha_inicio=fecha_cambio_cuatrimestre_anio_siguiente_2,
            fecha_fin=fecha_fin_anio_siguiente,
            anio_academico=anio_lectivo_siguiente,
            semestre=Semestres.SEGUNDO
        )
        segundo_semestre_anio_siguiente.full_clean()
        segundo_semestre_anio_siguiente.save()

        # Creo todos los bloques curriculares necesarios
        for bloque in NOMBRES_BLOQUES_CURRICULARES:
            bloque_curricular = BloqueCurricular(nombre=bloque, coeficiente=1.5)
            bloque_curricular.full_clean()
            bloque_curricular.save()

        # Creo las Asignaturas que serán compartidas:
        asignaturas_compartidas = []
        for info_asignatura in INFORMACION_ASIGNATURAS_COMPARTIDAS:
            asignatura = Asignatura(
                **info_asignatura,
                bloque_curricular=bloque_curricular
            )
            asignatura.full_clean()
            asignatura.save()
            asignaturas_compartidas.append(asignatura)

        # Creo los descriptores que seran compartidos
        descriptores_compartidos = []
        ejes_transversales_compartidos = []
        for i in range(3):
          descriptor = Descriptor(
              descripcion=f"Descriptor Compartido {i}",
              tipo=TipoDescriptor.DESCRIPTOR
          )
          descriptor.full_clean()
          descriptor.save()
          descriptores_compartidos.append(descriptor)

          eje_transversal = Descriptor(
              descripcion=f"Eje Transversal Compartido {i}",
              tipo=TipoDescriptor.EJE_TRANSVERSAL
          )
          eje_transversal.full_clean()
          eje_transversal.save()
          ejes_transversales_compartidos.append(eje_transversal)

        # Crear las carreras
        indice_carrera = 1
        for nombre_carrera in NOMBRES_CARRERAS:
            carrera = Carrera(nombre=nombre_carrera)
            carrera.full_clean()
            carrera.save()

            codigo_asignatura = "15_A{}{}"

            asignaturas_carrera = []
            indice_asignatura = 0
            for info_asignatura in INFORMACION_ASIGNATURAS_COMPARTIDAS:
                nueva_informacion = {**info_asignatura}
                nueva_informacion["codigo"] = codigo_asignatura.format(indice_carrera, indice_asignatura)
                nueva_informacion["bloque_curricular"] = bloque_curricular
                nueva_informacion["denominacion"] = f"Asignatura {carrera} {indice_asignatura}"
                asignatura = Asignatura(**nueva_informacion)
                asignatura.full_clean()
                asignatura.save()
                asignaturas_carrera.append(asignatura)
                indice_asignatura += 1

            descriptores_carrera = []
            ejes_transversales_carrera = []
            for i in range(2):
              descriptor = Descriptor(
              descripcion=f"Descriptor {i} - {carrera}",
                  tipo=TipoDescriptor.DESCRIPTOR
              )
              descriptor.full_clean()
              descriptor.save()
              descriptores_carrera.append(descriptor)

              eje_transversal = Descriptor(
                  descripcion=f"Eje {i} - {carrera}",
                  tipo=TipoDescriptor.EJE_TRANSVERSAL
              )
              eje_transversal.full_clean()
              eje_transversal.save()
              ejes_transversales_carrera.append(eje_transversal)

            # Creo un plan Activo y uno inactivo
            plan_inactivo = PlanDeEstudio(
                fecha_inicio = fecha_inicio_anio_anterior,
                fecha_fin=fecha_fin_anio_anterior,
                version=f"Version Plan {nombre_carrera} número 1.",
                nombre=f"Plan de Estudios {nombre_carrera}",
                carrera=carrera,
            )
            plan_inactivo.full_clean()
            plan_inactivo.save()
            plan_inactivo.asignaturas.set(asignaturas_carrera[:1] + asignaturas_compartidas)
            plan_inactivo.save()

            plan_activo = PlanDeEstudio(
                fecha_inicio = fecha_inicio_anio_actual,
                version=f"Version Plan {nombre_carrera} número 2.",
                nombre=f"Plan de Estudios {nombre_carrera}",
                carrera=carrera,
            )
            plan_activo.full_clean()
            plan_activo.save()
            plan_activo.asignaturas.set(asignaturas_carrera + asignaturas_compartidas)
            plan_activo.save()

            # Creo un estandar para la carrera
            estandar = Estandar(
                nombre=f"Estandar {nombre_carrera}",
                fecha_inicio=fecha_inicio_anio_anterior,
                carrera=carrera
            )
            estandar.full_clean()
            estandar.save()
            estandar.descriptores.set(descriptores_compartidos + ejes_transversales_compartidos + descriptores_carrera + ejes_transversales_carrera)
            estandar.save()


            # Creo actividades reservadas para el estandar
            for i in range(3):
                actividad_reservada = ActividadReservada(
                    estandar=estandar,
                    descripcion=f"Actividad Reservada {i} - {carrera}"
                )
                actividad_reservada.full_clean()
                actividad_reservada.save()

            indice_carrera += 1

