from freezegun import freeze_time
from datetime import time, datetime

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.common.mensajes_de_error import MENSAJE_NO_HAY_ANIO_ACTIVO
from backend.services import ServicioAnioAcademico
from backend.models import AnioAcademico
from backend.tests.utils import (
    crear_anios_de_prueba,
    FECHA_FIN_ANIO_ABIERTO,
    FECHA_FIN_ANIO_FUTURO,
)


class TestObtenerAnioAcademicoActual(TestCase):
    servicio_anio_academico = ServicioAnioAcademico()

    def setUp(self) -> None:
        (
            self.anio_cerrado,
            self.anio_actual,
            self.anio_futuro,
        ) = crear_anios_de_prueba()

    def test_probar_antes_de_media_noche_en_cambio_de_anio(self):
        hora_de_referencia = time(hour=23, minute=59, second=59)
        fecha_de_referencia = timezone.make_aware(
            datetime.combine(FECHA_FIN_ANIO_ABIERTO, hora_de_referencia)
        )
        with freeze_time(fecha_de_referencia):
            anio = self.servicio_anio_academico.obtener_anio_academico_actual()
        self.assertEqual(anio, self.anio_actual)

    def test_probar_despues_de_media_noche_en_cambio_de_anio(self):
        dia_de_referencia = FECHA_FIN_ANIO_ABIERTO + timezone.timedelta(days=1)
        hora_de_referencia = time(hour=0, minute=0, second=0)
        fecha_de_referencia = timezone.make_aware(
            datetime.combine(dia_de_referencia, hora_de_referencia)
        )
        with freeze_time(fecha_de_referencia):
            anio = self.servicio_anio_academico.obtener_anio_academico_actual()
        self.assertEqual(anio, self.anio_futuro)

    def test_no_se_crearon_anios(self):
        AnioAcademico.objects.all().delete()

        with self.assertRaises(ValidationError) as contexto:
            self.servicio_anio_academico.obtener_anio_academico_actual()

        self.assertIn("__all__", contexto.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_ANIO_ACTIVO,
            contexto.exception.message_dict["__all__"],
        )

    def test_no_hay_anio_actual(self):
        fecha_referencia = FECHA_FIN_ANIO_FUTURO + timezone.timedelta(days=7)
        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as contexto:
                self.servicio_anio_academico.obtener_anio_academico_actual()

            self.assertIn("__all__", contexto.exception.message_dict)
            self.assertIn(
                MENSAJE_NO_HAY_ANIO_ACTIVO,
                contexto.exception.message_dict["__all__"],
            )
