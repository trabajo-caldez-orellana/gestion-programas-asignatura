from freezegun import freeze_time
from datetime import time, datetime

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.common.mensajes_de_error import MENSAJE_NO_HAY_SEMESTRE_ACTIVO
from backend.services import ServicioSemestre
from backend.models import Semestre
from backend.tests.utils import (
    MENSAJE_SERVICIO_DEBE_FUNCIONAR_CORRECTAMENTE,
    crear_semestres_de_prueba,
    FECHA_INICIO_SEMESTRE_ABIERTO,
    FECHA_INICIO_SEMESTRE_CERRADO,
    FECHA_INICIO_SEMESTRE_FUTURO,
    FECHA_FIN_SEMESTRE_ABIERTO,
    FECHA_FIN_SEMESTRE_CERRADO,
    FECHA_FIN_SEMESTRE_FUTURO,
)


class TestObtenerSemestreActual(TestCase):
    servicio_semestre = ServicioSemestre()

    def setUp(self) -> None:
        (
            self.semestre_cerrado,
            self.semestre_actual,
            self.semestre_futuro,
        ) = crear_semestres_de_prueba()

    def test_probar_antes_de_media_noche_en_cambio_de_semestre(self):
        hora_de_referencia = time(hour=23, minute=59, second=59)
        fecha_de_referencia = timezone.make_aware(
            datetime.combine(FECHA_FIN_SEMESTRE_ABIERTO, hora_de_referencia)
        )
        with freeze_time(fecha_de_referencia):
            try:
                semestre = self.servicio_semestre.obtener_semestre_actual()
            except Exception as e:
                self.fail(MENSAJE_SERVICIO_DEBE_FUNCIONAR_CORRECTAMENTE)

        self.assertEqual(semestre, self.semestre_actual)

    def test_probar_despues_de_media_noche_en_cambio_de_semestre(self):
        dia_de_referencia = FECHA_FIN_SEMESTRE_ABIERTO + timezone.timedelta(days=1)
        hora_de_referencia = time(hour=0, minute=0, second=0)
        fecha_de_referencia = timezone.make_aware(
            datetime.combine(dia_de_referencia, hora_de_referencia)
        )
        with freeze_time(fecha_de_referencia):
            try:
                semestre = self.servicio_semestre.obtener_semestre_actual()
            except Exception as e:
                self.fail(MENSAJE_SERVICIO_DEBE_FUNCIONAR_CORRECTAMENTE)
        self.assertEqual(semestre, self.semestre_futuro)

    def test_no_se_crearon_semestres(self):
        Semestre.objects.all().delete()

        with self.assertRaises(ValidationError) as contexto:
            semestre = self.servicio_semestre.obtener_semestre_actual()

        self.assertIn("__all__", contexto.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRE_ACTIVO,
            contexto.exception.message_dict["__all__"],
        )

    def test_no_hay_semestre_actual(self):
        fecha_referencia = FECHA_FIN_SEMESTRE_FUTURO + timezone.timedelta(days=7)
        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as contexto:
                semestre = self.servicio_semestre.obtener_semestre_actual()

                self.assertIn("__all__", contexto.exception.message_dict)
                self.assertIn(
                    MENSAJE_NO_HAY_SEMESTRE_ACTIVO,
                    contexto.exception.message_dict["__all__"],
                )
