from freezegun import freeze_time

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from backend.services import ServicioConfiguracion
from backend.tests.utils import (
    crear_semestres_de_prueba,
    crear_fecha_y_hora,
    crear_configuraciones_del_prograna,
    FECHA_DEFAULT_VALIDACION,
)
from backend.common.mensajes_de_error import (
    MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
    MENSAJE_NO_FUE_DEFINIDO_PERIODO_VALIDACION,
)


class TestObtenerDiasRestantesInicioPeriodoValidacion(TestCase):
    servicio_configuracion = ServicioConfiguracion()

    def test_no_hay_semestre_siguiente(self):
        crear_configuraciones_del_prograna()
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        semestre_siguiente.delete()
        with self.assertRaises(ValidationError) as exepcion:
            self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_de_validacion()

        self.assertIn("__all__", exepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
            exepcion.exception.message_dict["__all__"],
        )

    def test_no_fue_creada_la_configuracion_necesaria(self):
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        semestre_siguiente.delete()
        with self.assertRaises(ValidationError) as exepcion:
            self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_de_validacion()

        self.assertIn("__all__", exepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_FUE_DEFINIDO_PERIODO_VALIDACION,
            exepcion.exception.message_dict["__all__"],
        )

    def test_ultimo_segundo_antes_del_inicio(self):
        crear_configuraciones_del_prograna()
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        dia_anterior_inicio_periodo = (
            semestre_siguiente.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_VALIDACION + 1)
        )
        fecha_referencia = crear_fecha_y_hora(
            anio=dia_anterior_inicio_periodo.year,
            mes=dia_anterior_inicio_periodo.month,
            dia=dia_anterior_inicio_periodo.day,
            hora=23,
            minuto=59,
            segundo=59,
        )

        with freeze_time(fecha_referencia):
            dias_restantes = (
                self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_de_validacion()
            )

            self.assertEqual(dias_restantes, 1)

    def test_periodo_de_modificacion_iniciado(self):
        crear_configuraciones_del_prograna()
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        dia_anterior_inicio_periodo = (
            semestre_siguiente.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_VALIDACION)
        )
        fecha_referencia = crear_fecha_y_hora(
            anio=dia_anterior_inicio_periodo.year,
            mes=dia_anterior_inicio_periodo.month,
            dia=dia_anterior_inicio_periodo.day,
        )

        with freeze_time(fecha_referencia):
            dias_restantes = (
                self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_de_validacion()
            )

            self.assertEqual(dias_restantes, 0)

    def test_no_hay_semestres_creados(self):
        crear_configuraciones_del_prograna()

        with self.assertRaises(ValidationError) as exepcion:
            self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_de_validacion()

        self.assertIn("__all__", exepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
            exepcion.exception.message_dict["__all__"],
        )

    def test_no_hay_semestre_actual(self):
        crear_configuraciones_del_prograna()
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        semestre_actual.delete()
        with self.assertRaises(ValidationError) as exepcion:
            self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_de_validacion()

        self.assertIn("__all__", exepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
            exepcion.exception.message_dict["__all__"],
        )
