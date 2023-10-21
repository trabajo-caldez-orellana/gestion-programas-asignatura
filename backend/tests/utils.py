import json

from django.utils import timezone

from backend.models import (
    Carrera,
    Estandar,
    PlanDeEstudio,
    Asignatura,
    BloqueCurricular,
    ActividadReservada,
    Descriptor,
    Semestre,
    VersionProgramaAsignatura,
    ProgramaTieneActividadReservada,
    ProgramaTieneDescriptor,
    CargaBloque,
)
from backend.common.choices import (
    MetodologiaAsignatura,
    TipoDescriptor,
    EstadoAsignatura,
    NivelDescriptor,
)
from backend.common.constantes import MINIMO_RESULTADOS_DE_APRENDIZAJE


CODIGO_ASIGNATURA_1 = "15_SIM"
CODIGO_ASIGNATURA_2 = "15_TER"
CODIGO_ASIGNATURA_COMPARTIDA = "15_XC1"
CARRERA_1 = "Ingenieria en Computacion"
CARRERA_2 = "Ingenieria Quimica"


# FUNCIONES PARA EL SETUP
def set_up_tests():
    """
    Crea:
     - Dos carreras
     - Dos bloques curriculares
     - Una asignatura para cada carrera, y una compartida entre ambas carreras
     - Un plan de estudio activo para cada carrera
     - Cinco descriptores, dos para cada estandar (uno de cada tipo), y uno compartido
     - Un estandar activo para cada carrera
     - Dos actividades reservadas para cada estandar
     - Crea un semestre acutal, y uno anterior
    """

    # Crear dos carreras
    carrera_1 = Carrera.objects.create(nombre=CARRERA_1)
    carrera_2 = Carrera.objects.create(nombre=CARRERA_2)

    hoy = timezone.now().astimezone()
    fecha_inicio = hoy - timezone.timedelta(days=1)

    # Creo bloques curriculares
    bloque_curricular_1 = BloqueCurricular.objects.create(
        nombre="Ciencias Básicas", coeficiente=1.5
    )
    bloque_curricular_2 = BloqueCurricular.objects.create(
        nombre="Tecnologías Básicas", coeficiente=2
    )

    # Creo las asignaturas
    asignatura_carrera_1 = Asignatura.objects.create(
        denominacion="Sistemas con Micro",
        codigo=CODIGO_ASIGNATURA_1,
        metodologia=MetodologiaAsignatura.PRESENCIAL,
        bloque_curricular=bloque_curricular_1,
    )

    asignatura_carrera_2 = Asignatura.objects.create(
        denominacion="Termodinamica",
        codigo=CODIGO_ASIGNATURA_2,
        metodologia=MetodologiaAsignatura.PRESENCIAL,
        bloque_curricular=bloque_curricular_2,
    )

    asignatura_compartida = Asignatura.objects.create(
        denominacion="Calculo I",
        codigo=CODIGO_ASIGNATURA_COMPARTIDA,
        metodologia=MetodologiaAsignatura.PRESENCIAL,
        bloque_curricular=bloque_curricular_1,
    )

    # Crea dos planes de estudio activos, uno para carrera
    plan_carrera_1 = PlanDeEstudio.objects.create(
        carrera=carrera_1,
        fecha_inicio=fecha_inicio,
        version="1",
        nombre="Plan de estudio Ingenieria en Computacion",
    )
    plan_carrera_1.asignaturas.set([asignatura_carrera_1, asignatura_compartida])
    plan_carrera_1.full_clean()
    plan_carrera_1.save()

    plan_carrera_2 = PlanDeEstudio.objects.create(
        carrera=carrera_2,
        fecha_inicio=fecha_inicio,
        version="1",
        nombre="Plan de estudio Ingenieria Química",
    )
    plan_carrera_2.asignaturas.set([asignatura_carrera_2, asignatura_compartida])
    plan_carrera_2.full_clean()
    plan_carrera_2.save()

    # Descriptores
    descriptor_carrera_1 = Descriptor.objects.create(
        descripcion="Descriptor Ing. Comuntación", tipo=TipoDescriptor.DESCRIPTOR
    )
    descriptor_carrera_2 = Descriptor.objects.create(
        descripcion="Descriptor Ing. Química", tipo=TipoDescriptor.DESCRIPTOR
    )
    eje_carrera_1 = Descriptor.objects.create(
        descripcion="Eje Transversal Ing. Comuntación",
        tipo=TipoDescriptor.EJE_TRANSVERSAL,
    )
    eje_carrera_2 = Descriptor.objects.create(
        descripcion="Eje Transversal Ing. Química", tipo=TipoDescriptor.EJE_TRANSVERSAL
    )
    descriptor_compartido = Descriptor.objects.create(
        descripcion="Descriptor compartido", tipo=TipoDescriptor.DESCRIPTOR
    )

    # Crear dos estándares activos. Para que los tests corran correctamente, los estándares
    # comenzarán el día anterior del momento en que se corran los tests
    estandar_carrera_1 = Estandar.objects.create(
        carrera=carrera_1,
        nombre="Estandar Ingeniería en Computación",
        fecha_inicio=fecha_inicio,
    )
    estandar_carrera_1.descriptores.set(
        [descriptor_carrera_1, eje_carrera_1, descriptor_compartido]
    )
    estandar_carrera_1.full_clean()
    estandar_carrera_1.save()

    estandar_carrera_2 = Estandar.objects.create(
        carrera=carrera_2,
        nombre="Estandar Ingeniería Química",
        fecha_inicio=fecha_inicio,
    )
    estandar_carrera_2.descriptores.set(
        [descriptor_carrera_2, eje_carrera_2, descriptor_compartido]
    )
    estandar_carrera_2.full_clean()
    estandar_carrera_2.save()

    # Actividades reservadas
    actividad_1_carrera_1 = ActividadReservada.objects.create(
        descripcion="Actividad Reservada 1 Ingenieria En Computacion",
        estandar=estandar_carrera_1,
    )
    actividad_2_carrera_1 = ActividadReservada.objects.create(
        descripcion="Actividad Reservada 2 Ingenieria En Computacion",
        estandar=estandar_carrera_1,
    )
    actividad_1_carrera_2 = ActividadReservada.objects.create(
        descripcion="Actividad Reservada 1 Ingenieria Química",
        estandar=estandar_carrera_2,
    )
    actividad_2_carrera_2 = ActividadReservada.objects.create(
        descripcion="Actividad Reservada 2 Ingenieria Química",
        estandar=estandar_carrera_2,
    )

    # Crea un semestre actual
    fecha_fin_semestre = fecha_inicio + timezone.timedelta(days=7 * 4)
    semestre = Semestre.objects.create(
        fecha_inicio=fecha_inicio, fecha_fin=fecha_fin_semestre
    )

    # Crea un semestre anterior
    fecha_inicio_semestre_anterior = fecha_inicio - timezone.timedelta(days=7 * 4)
    fecha_fin_semestre_anterior = fecha_inicio - timezone.timedelta(days=1)
    semestre_anterior = Semestre.objects.create(
        fecha_inicio=fecha_fin_semestre_anterior, fecha_fin=fecha_fin_semestre_anterior
    )


def crear_programa_de_asignatura(
    asignatura: Asignatura,
    semestre: Semestre,
    carrera: Carrera,
    esta_aprobado: bool = True,
):
    datos_programa = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
    datos_programa["semestre"] = semestre
    datos_programa["asignatura"] = asignatura

    if not esta_aprobado:
        datos_programa["estado"] = EstadoAsignatura.ABIERTO

    programa = VersionProgramaAsignatura.objects.create(**datos_programa)
    estandar_carrera = Estandar.objects.get(carrera=carrera)

    # Agrego actividades reservadas
    actividades_reservadas_carrera = ActividadReservada.objects.filter(
        estandar=estandar_carrera
    )
    ProgramaTieneActividadReservada.objects.create(
        version_programa_asignatura=programa,
        actividad_reservada=actividades_reservadas_carrera.first(),
        nivel=NivelDescriptor.BAJO,
    )

    descriptores_carrera = estandar_carrera.descriptores.all()
    # Agrego ejes transversales
    ejes_transversales = descriptores_carrera.filter(
        tipo=TipoDescriptor.EJE_TRANSVERSAL
    )
    for eje in ejes_transversales:
        ProgramaTieneDescriptor.objects.create(
            descriptor=eje,
            version_programa_asignatura=programa,
            nivel=NivelDescriptor.BAJO,
        )

    # Agrego descriptores
    descriptores = descriptores_carrera.filter(tipo=TipoDescriptor.DESCRIPTOR)
    for descriptor in descriptores:
        ProgramaTieneDescriptor.objects.create(
            descriptor=descriptor,
            version_programa_asignatura=programa,
            nivel=NivelDescriptor.BAJO,
        )

    # Agrego carga horaria al bloque
    carga_bloque = CargaBloque.objects.create(
        horas=20,
        version_programa_asignatura=programa,
        bloque_curricular=asignatura.bloque_curricular,
    )

    return programa


# VALORES DEFAULT
DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE = [
    "Resultado de aprendizaje 1",
    "Resultado de aprendizaje 2",
    "Resultado de aprendizaje 3",
    "Resultado de aprendizaje 4",
    "Resultado de aprendizaje 5",
    "Resultado de aprendizaje 6",
    "Resultado de aprendizaje 7",
    "Resultado de aprendizaje 8",
    "Resultado de aprendizaje 9",
    "Resultado de aprendizaje 10",
]

DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA = {
    "estado": EstadoAsignatura.APROBADO,
    "semanas_dictado": 16,
    "semanal_teoria_presencial": 4,
    "semanal_practica_presencial": 4,
    "semanal_teorico_practico_presencial": 0,
    "semanal_lab_presencial": 0,
    "contenidos": "CONTENIDO DE EJEMPLO",
    "bibliografia": "BIBLIOGRAFIA DE EJEMPLO",
    "recursos": "RECURSOS DE EJEMPLO",
    "evaluacion": "EVALUACION DE EJEMPLO",
    "investigacion_docentes": "EJEMPLO",
    "investigacion_estudiantes": "EJEMPLO",
    "extension_docentes": "EJEMPLO",
    "extension_estudiantes": "EJEMPLO",
    "cronograma": "CRONOGRAMA DE EJEMPLO",
    "resultados_de_aprendizaje": json.dumps(
        DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[:MINIMO_RESULTADOS_DE_APRENDIZAJE]
    ),
}

# Mensajes de error para asserts
MENSAJE_SERVICIO_DEBE_FALLAR = "El servicio debe fallar."
MENSAJE_SERVICIO_DEBE_FUNCIONAR_CORRECTAMENTE = (
    "El servicio debe funcionar correctamente sin excepciones"
)
