from freezegun import freeze_time

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from backend.services import ServicioConfiguracion
from backend.tests.utils import crear_semestres_de_prueba, crear_fecha_y_hora
from backend.common.mensajes_de_error import MENSAJE_NO_HAY_SEMESTRES_FUTUROS


class TestObtenerDiasRestantesInicioSiguienteSemestre(TestCase):
    servicio_configuracion = ServicioConfiguracion()

    def test_no_hay_semestre_siguiente(self):
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        fecha_referencia = crear_fecha_y_hora(
            anio=semestre_siguiente.fecha_inicio.year,
            mes=semestre_siguiente.fecha_inicio.month,
            dia=semestre_siguiente.fecha_inicio.day,
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as exepcion:
                self.servicio_configuracion.obtener_dias_restantes_inicio_siguiente_semestre()

            self.assertIn("__all__", exepcion.exception.message_dict)
            self.assertIn(
                MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
                exepcion.exception.message_dict["__all__"],
            )

    def test_probar_ultimo_segundo_antes_del_inicio(self):
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        dia_anterior = semestre_siguiente.fecha_inicio - timezone.timedelta(days=1)
        fecha_referencia = crear_fecha_y_hora(
            anio=dia_anterior.year,
            mes=dia_anterior.month,
            dia=dia_anterior.day,
            hora=23,
            minuto=59,
            segundo=59,
        )

        with freeze_time(fecha_referencia):
            dias_restantes = (
                self.servicio_configuracion.obtener_dias_restantes_inicio_siguiente_semestre()
            )

            self.assertEqual(dias_restantes, 1)

    def test_no_hay_semestres_creados(self):
        with self.assertRaises(ValidationError) as exepcion:
            self.servicio_configuracion.obtener_dias_restantes_inicio_siguiente_semestre()

        self.assertIn("__all__", exepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
            exepcion.exception.message_dict["__all__"],
        )

    def test_no_hay_semestre_actual(self):
        (
            semestre_anterior,
            semestre_actual,
            semestre_siguiente,
        ) = crear_semestres_de_prueba()

        semestre_actual.delete()
        with self.assertRaises(ValidationError) as exepcion:
            self.servicio_configuracion.obtener_dias_restantes_inicio_siguiente_semestre()

        self.assertIn("__all__", exepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
            exepcion.exception.message_dict["__all__"],
        )
