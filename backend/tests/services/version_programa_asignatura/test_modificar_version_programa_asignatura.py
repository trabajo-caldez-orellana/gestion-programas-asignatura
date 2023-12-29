import json
from freezegun import freeze_time

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from backend.services import ServicioVersionProgramaAsignatura
from backend.tests.utils import (
    set_up_tests,
    VALORES_INVALIDOS,
    CODIGO_ASIGNATURA_1,
    CODIGO_ASIGNATURA_2,
    CARRERA_1,
    CARRERA_2,
    DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE,
    NOMBRE_DESCRIPTOR_1,
    NOMBRE_DESCRIPTOR_2,
    NOMBRE_DESCRIPTOR_COMPARTIDO,
    NOMBRE_EJE_1,
    NOMBRE_EJE_2,
    NOMBRE_ACTIVIDAD_1_CARRERA_1,
    NOMBRE_ACTIVIDAD_2_CARRERA_1,
    NOMBRE_ACTIVIDAD_1_CARRERA_2,
    NOMBRE_ACTIVIDAD_2_CARRERA_2,
    FECHA_DEFAULT_MODIFICACION,
    FECHA_INICIO_SEMESTRE_FUTURO,
    FECHA_INICIO_SEMESTRE_ABIERTO,
    crear_configuraciones_del_prograna,
    crear_semestres_de_prueba,
    crear_fecha_y_hora,
)
from backend.models import (
    Asignatura,
    Descriptor,
    Carrera,
    ActividadReservada,
    VersionProgramaAsignatura,
)
from backend.common.mensajes_de_error import (
    MENSAJE_DESCRIPTOR,
    MENSAJE_ACTIVIDAD_RESERVADA,
    MENSAJE_EJE_TRANSVERAL,
    MENSAJE_CANTIDAD_DE_RESULTADOS,
    MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR,
    MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
    MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
    MENSAJE_FORMATO_DESCRIPTORES_INVALIDO,
    MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO,
    MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO,
    MENSAJE_DESCRIPTOR_INVALIDO,
    MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA,
    MENSAJE_EJE_TRANSVERSAL_INVALIDO,
    MENSAJE_NIVEL_INVALIDO,
    MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO,
    MENSAJE_CAMPO_NO_NULO,
    MENSAJE_CAMPO_EN_BLANCO,
    MENSAJE_PROGRAMAS_CERRADOS,
    MENSAJE_NIVEL_INCORRECTO,
)
from backend.common.choices import NivelDescriptor, TipoDescriptor, Semestres
from backend.common.constantes import (
    MINIMO_RESULTADOS_DE_APRENDIZAJE,
    MAXIMO_RESULTADOS_DE_APRENDIZAJE,
)


PROGRAMA_FORMATO_DEFAULT = {
    "descriptores": [],
    "actividades_reservadas": [],
    "ejes_transversales": [],
    "resultados_de_aprendizaje": json.dumps(
        DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[:MINIMO_RESULTADOS_DE_APRENDIZAJE]
    ),
    "contenidos": "Texto de ejemplo",
    "bibliografia": "Texto de ejemplo",
    "recursos": "Texto de ejemplo",
    "evaluacion": "Texto de ejemplo",
    "investigacion_docentes": "Texto de ejemplo",
    "investigacion_estudiantes": "Texto de ejemplo",
    "extension_docentes": "Texto de ejemplo",
    "extension_estudiantes": "Texto de ejemplo",
    "cronograma": "Texto de ejemplo",
}


class TestModificarPrograma(TestCase):
    servicio_version_programa_asignatura = ServicioVersionProgramaAsignatura()

    def setUp(self):
        set_up_tests()
        crear_configuraciones_del_prograna()
        crear_semestres_de_prueba()

        self.asignatura_1 = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_1)
        self.asignatura_2 = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_2)
        self.carrera_1 = Carrera.objects.get(nombre=CARRERA_1)
        self.carrera_2 = Carrera.objects.get(nombre=CARRERA_2)

        # Obtengo los descriptores correspondientes a la primera asignatura
        self.descriptores_1 = Descriptor.objects.filter(
            tipo=TipoDescriptor.DESCRIPTOR,
            descripcion__in=[NOMBRE_DESCRIPTOR_1, NOMBRE_DESCRIPTOR_COMPARTIDO],
        )
        self.descriptores_2 = Descriptor.objects.filter(
            tipo=TipoDescriptor.DESCRIPTOR,
            descripcion__in=[NOMBRE_DESCRIPTOR_2, NOMBRE_DESCRIPTOR_COMPARTIDO],
        )

        self.eje_transversal_1 = Descriptor.objects.get(
            tipo=TipoDescriptor.EJE_TRANSVERSAL, descripcion=NOMBRE_EJE_1
        )
        self.eje_transversal_2 = Descriptor.objects.get(
            tipo=TipoDescriptor.EJE_TRANSVERSAL, descripcion=NOMBRE_EJE_2
        )

        self.actividades_reservadas_1 = ActividadReservada.objects.filter(
            descripcion__in=[NOMBRE_ACTIVIDAD_1_CARRERA_1, NOMBRE_ACTIVIDAD_2_CARRERA_1]
        )
        self.actividades_reservadas_2 = ActividadReservada.objects.filter(
            descripcion__in=[NOMBRE_ACTIVIDAD_1_CARRERA_2, NOMBRE_ACTIVIDAD_2_CARRERA_2]
        )

    def _crear_lista_descriptores_asignatura_1(self):
        return [
            {"id": descriptor.id, "nivel": NivelDescriptor.BAJO}
            for descriptor in self.descriptores_1
        ]

    def _crear_lista_descriptores_asignatura_2(self):
        return [
            {"id": descriptor.id, "nivel": NivelDescriptor.BAJO}
            for descriptor in self.descriptores_2
        ]

    def _crear_lista_eje_transversal_asignatura_1(self):
        return [{"id": self.eje_transversal_1.id, "nivel": NivelDescriptor.ALTO}]

    def _crear_lista_eje_transversal_asignatura_2(self):
        return [{"id": self.eje_transversal_2.id, "nivel": NivelDescriptor.ALTO}]

    def _crear_lista_actividades_reservadas_asignatura_1(self):
        return [
            {"id": actividad.id, "nivel": NivelDescriptor.ALTO}
            for actividad in self.actividades_reservadas_1
        ]

    def _crear_lista_actividades_reservadas_asignatura_2(self):
        return [
            {"id": actividad.id, "nivel": NivelDescriptor.ALTO}
            for actividad in self.actividades_reservadas_2
        ]

    def _validar_modificacion_incorreacta(self, parametros, error, mensaje_de_error):
        try:
            self.servicio_version_programa_asignatura.modificar_version_programa_asignatura(
                **parametros
            )
        except ValidationError as e:
            self.assertIn(error, e.message_dict)
            self.assertIn(mensaje_de_error, e.message_dict[error])

    def _crear_programa_de_asignatura(self) -> VersionProgramaAsignatura:
        fecha_de_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )
        fecha_de_referencia = crear_fecha_y_hora(
            anio=fecha_de_referencia.year,
            mes=fecha_de_referencia.month,
            dia=fecha_de_referencia.day,
        )

        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "asignatura": self.asignatura_1,
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        with freeze_time(fecha_de_referencia):
            version_programa = self.servicio_version_programa_asignatura.crear_nueva_version_programa_asignatura(
                **parametros
            )

        return version_programa

    def test_no_es_periodo_de_actualizacion_de_programas(self):
        fecha_de_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION + 1
        )
        fecha_de_referencia = crear_fecha_y_hora(
            anio=fecha_de_referencia.year,
            mes=fecha_de_referencia.month,
            dia=fecha_de_referencia.day,
        )

        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        self._validar_modificacion_incorreacta(
            parametros, "__all__", MENSAJE_PROGRAMAS_CERRADOS
        )

        # Ahora no es posible porque la materia es de primer cuatrimestre y el siguiente
        # semestre es el segundo
        self.asignatura_1.semestre_dictado = Semestres.PRIMER
        self.asignatura_1.full_clean()
        self.asignatura_1.save()

        self._validar_modificacion_incorreacta(
            parametros, "__all__", MENSAJE_PROGRAMAS_CERRADOS
        )

        # Ahora no es posible porque la materia es de segundo cuatrimestre y el siguiente
        # semestre es el primero
        fecha_de_referencia = FECHA_INICIO_SEMESTRE_ABIERTO - timezone.timedelta(days=1)
        fecha_de_referencia = crear_fecha_y_hora(
            anio=fecha_de_referencia.year,
            mes=fecha_de_referencia.month,
            dia=fecha_de_referencia.day,
        )

        with freeze_time(fecha_de_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "__all__", MENSAJE_PROGRAMAS_CERRADOS
            )

    def test_descriptores_invalidos(self):
        """
        La lista de descriptores que se manda tiene formato incorrecto, o los ID provistos son inexistentes
        """
        fecha_de_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )
        fecha_de_referencia = crear_fecha_y_hora(
            anio=fecha_de_referencia.year,
            mes=fecha_de_referencia.month,
            dia=fecha_de_referencia.day,
        )

        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
        }

        # No agrega ningun descriptor
        with freeze_time(fecha_de_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "descriptores", MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR
            )

        arrays_con_formatos_invalidos = [
            [self.eje_transversal_1.id],
            [{"id": self.eje_transversal_1.id}],
            [{"valor": NivelDescriptor.ALTO}],
            [{"id": self.eje_transversal_1.id}],
        ]

        for formato_actividades_invalido in arrays_con_formatos_invalidos:
            parametros["descriptores"] = formato_actividades_invalido

            with freeze_time(fecha_de_referencia):
                self._validar_modificacion_incorreacta(
                    parametros,
                    "descriptores",
                    MENSAJE_FORMATO_DESCRIPTORES_INVALIDO,
                )

        # Primero formato invalido de descriptores:
        formato_descriptores_invalido = [
            descriptor.id for descriptor in self.descriptores_1
        ]

        parametros["descriptores"] = formato_descriptores_invalido
        with freeze_time(fecha_de_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "descriptores", MENSAJE_FORMATO_DESCRIPTORES_INVALIDO
            )

        # Id inexistente
        parametros["descriptores"] = [{"id": 100, "nivel": NivelDescriptor.BAJO}]
        with freeze_time(fecha_de_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "descriptores", MENSAJE_DESCRIPTOR_INVALIDO
            )

    def test_descriptor_de_otra_carrera(self):
        """
        Los ids provistos pertenecen a descriptores de otra carrera
        """
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_2(),
        }
        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )
        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "descriptores", MENSAJE_DESCRIPTOR
            )

    def test_actividades_reservadas_invalidas(self):
        """
        La lista de actividades reservadas que se manda tiene formato incorrecto, o los ID provistos son inexistentes
        """
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        # No agrega ninguna actividad reservada
        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros,
                "actividades_reservadas",
                MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
            )

        arrays_con_formatos_invalidos = [
            [actividad.id for actividad in self.actividades_reservadas_1],
            [{"id": actividad.id} for actividad in self.actividades_reservadas_1],
            [
                {"valor": NivelDescriptor.ALTO}
                for actividad in self.actividades_reservadas_1
            ],
            [{"id": actividad.id} for actividad in self.actividades_reservadas_1],
        ]

        for formato_actividades_invalido in arrays_con_formatos_invalidos:
            parametros["actividades_reservadas"] = formato_actividades_invalido

            with freeze_time(fecha_referencia):
                self._validar_modificacion_incorreacta(
                    parametros,
                    "actividades_reservadas",
                    MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO,
                )

        # Id inexistente
        parametros["actividades_reservadas"] = [
            {"id": 100, "nivel": NivelDescriptor.ALTO}
        ]

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros,
                "actividades_reservadas",
                MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA,
            )

    def test_actividad_reservada_de_otra_carrera(self):
        """
        Los ids provistos pertenecen a actividades reservadas de otra carrera
        """
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_2(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "actividades_reservadas", MENSAJE_ACTIVIDAD_RESERVADA
            )

    def test_nivel_actividad_reservada_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": [
                {"id": actividad.id, "nivel": "invalid"}
                for actividad in self.actividades_reservadas_1
            ],
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "actividades_reservadas", MENSAJE_NIVEL_INVALIDO
            )

        parametros["actividades_reservadas"] = [
            {"id": actividad.id, "nivel": 10}
            for actividad in self.actividades_reservadas_1
        ]

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "actividades_reservadas", MENSAJE_NIVEL_INVALIDO
            )

    def test_ejes_transversales_invalidos(self):
        """
        La lista de ejes transversales que se manda tiene formato incorrecto, o los ID provistos son inexistentes
        """
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        # No agrega ningun eje transversal
        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros,
                "ejes_transversales",
                MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
            )

        arrays_con_formatos_invalidos = [
            [self.eje_transversal_1.id],
            [{"id": self.eje_transversal_1.id}],
            [{"valor": NivelDescriptor.ALTO}],
            [{"id": self.eje_transversal_1.id}],
        ]

        for formato_actividades_invalido in arrays_con_formatos_invalidos:
            parametros["ejes_transversales"] = formato_actividades_invalido

            with freeze_time(fecha_referencia):
                self._validar_modificacion_incorreacta(
                    parametros,
                    "ejes_transversales",
                    MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO,
                )

        arrays_con_niveles_invalidos = [
            [{"id": self.eje_transversal_1.id, "nivel": "invalid"}],
            [{"id": self.eje_transversal_1.id, "nivel": 10}],
        ]

        for formato_actividades_invalido in arrays_con_niveles_invalidos:
            parametros["ejes_transversales"] = formato_actividades_invalido

            with freeze_time(fecha_referencia):
                self._validar_modificacion_incorreacta(
                    parametros,
                    "ejes_transversales",
                    MENSAJE_NIVEL_INVALIDO,
                )

        # Id inexistente
        parametros["ejes_transversales"] = [{"id": 100, "nivel": NivelDescriptor.ALTO}]
        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "ejes_transversales", MENSAJE_EJE_TRANSVERSAL_INVALIDO
            )

    def test_eje_de_otra_carrera(self):
        """
        Los ids provistos pertenecen a ejes transversales de otra carrera
        """
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_2(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros, "ejes_transversales", MENSAJE_EJE_TRANSVERAL
            )

    def test_valor_resultados_de_aprendizaje_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        valores_invalidos = VALORES_INVALIDOS + [json.dumps({})]
        for valor in valores_invalidos:
            parametros["resultados_de_aprendizaje"] = valor

            with freeze_time(fecha_referencia):
                self._validar_modificacion_incorreacta(
                    parametros,
                    "resultados_de_aprendizaje",
                    MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO,
                )

    def test_cantidad_de_resultados_menor_al_minimo(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
            "resultados_de_aprendizaje": json.dumps(
                DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[
                    : MINIMO_RESULTADOS_DE_APRENDIZAJE - 1
                ]
            ),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros,
                "resultados_de_aprendizaje",
                MENSAJE_CANTIDAD_DE_RESULTADOS,
            )

    def test_cantidad_de_resultados_mayor_al_maximo(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
            "resultados_de_aprendizaje": json.dumps(
                DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[
                    : MAXIMO_RESULTADOS_DE_APRENDIZAJE + 1
                ]
            ),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            self._validar_modificacion_incorreacta(
                parametros,
                "resultados_de_aprendizaje",
                MENSAJE_CANTIDAD_DE_RESULTADOS,
            )

    def test_valor_contenidos_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["contenidos"] = None
            self._validar_modificacion_incorreacta(
                parametros, "contenidos", MENSAJE_CAMPO_NO_NULO
            )

            parametros["contenidos"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "contenidos", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_bibliografia_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["bibliografia"] = None
            self._validar_modificacion_incorreacta(
                parametros, "bibliografia", MENSAJE_CAMPO_NO_NULO
            )

            parametros["bibliografia"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "bibliografia", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_recursos_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["recursos"] = None
            self._validar_modificacion_incorreacta(
                parametros, "recursos", MENSAJE_CAMPO_NO_NULO
            )

            parametros["recursos"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "recursos", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_evaluacion_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["evaluacion"] = None
            self._validar_modificacion_incorreacta(
                parametros, "evaluacion", MENSAJE_CAMPO_NO_NULO
            )

            parametros["evaluacion"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "evaluacion", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_investigacion_docentes_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["investigacion_docentes"] = None
            self._validar_modificacion_incorreacta(
                parametros, "investigacion_docentes", MENSAJE_CAMPO_NO_NULO
            )

            parametros["investigacion_docentes"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "investigacion_docentes", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_investigacion_estudiantes_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["investigacion_estudiantes"] = None
            self._validar_modificacion_incorreacta(
                parametros, "investigacion_estudiantes", MENSAJE_CAMPO_NO_NULO
            )

            parametros["investigacion_estudiantes"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "investigacion_estudiantes", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_extension_docentes_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["extension_docentes"] = None
            self._validar_modificacion_incorreacta(
                parametros, "extension_docentes", MENSAJE_CAMPO_NO_NULO
            )

            parametros["extension_docentes"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "extension_docentes", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_extension_estudiantes_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "version_programa": self._crear_programa_de_asignatura(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["extension_estudiantes"] = None
            self._validar_modificacion_incorreacta(
                parametros, "extension_estudiantes", MENSAJE_CAMPO_NO_NULO
            )

            parametros["extension_estudiantes"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "extension_estudiantes", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_valor_cronograma_invalido(self):
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "descriptores": self._crear_lista_descriptores_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        with freeze_time(fecha_referencia):
            parametros["cronograma"] = None
            self._validar_modificacion_incorreacta(
                parametros, "cronograma", MENSAJE_CAMPO_NO_NULO
            )

            parametros["cronograma"] = ""
            self._validar_modificacion_incorreacta(
                parametros, "cronograma", MENSAJE_CAMPO_EN_BLANCO
            )

    def test_asignar_nivel_invalido_a_descriptor(self):
        """
        La lista de descriptores que se manda tiene algun nivel incorrecto para el descriptor
        """
        parametros = {
            **PROGRAMA_FORMATO_DEFAULT,
            "version_programa": self._crear_programa_de_asignatura(),
            "ejes_transversales": self._crear_lista_eje_transversal_asignatura_1(),
            "actividades_reservadas": self._crear_lista_actividades_reservadas_asignatura_1(),
        }

        fecha_referencia = FECHA_INICIO_SEMESTRE_FUTURO - timezone.timedelta(
            days=FECHA_DEFAULT_MODIFICACION - 1
        )

        arrays_con_niveles_invalidos = [
            [{"id": self.descriptores_1[0].id, "nivel": NivelDescriptor.MEDIO}],
            [{"id": self.descriptores_1[0].id, "nivel": NivelDescriptor.ALTO}],
        ]

        for formato_descriptores_invalido in arrays_con_niveles_invalidos:
            parametros["descriptores"] = formato_descriptores_invalido

            with freeze_time(fecha_referencia):
                self._validar_modificacion_incorreacta(
                    parametros,
                    "descriptores",
                    MENSAJE_NIVEL_INCORRECTO,
                )
