from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import AnioAcademico
from backend.services import ServicioAnioAcademico
from backend.common.mensajes_de_error import (
    MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
    MENSAJE_FECHAS_INCORRECTAS,
)


class TestValidarAnioAcademico(TestCase):
    servicio_anio_academico = ServicioAnioAcademico()

    def test_no_hay_anioss_creados(self):
        self.servicio_anio_academico.validar_anio_academico(
            fecha_inicio=timezone.datetime(day=1, month=7, year=2023),
            fecha_fin=timezone.datetime(day=31, month=12, year=2023),
        )

    def test_coincide_primer_dia(self):
        primer_dia = timezone.datetime(day=1, month=7, year=2023)
        ultimo_dia = timezone.datetime(day=31, month=12, year=2023)
        AnioAcademico.objects.create(fecha_inicio=primer_dia, fecha_fin=ultimo_dia)

        with self.assertRaises(ValidationError) as context:
            self.servicio_anio_academico.validar_anio_academico(
                fecha_inicio=ultimo_dia,
                fecha_fin=timezone.datetime(day=30, month=6, year=2024),
            )

        self.assertIn("fecha_inicio", context.exception.message_dict)
        self.assertIn("fecha_fin", context.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_inicio"),
        )
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_fin"),
        )

    def test_coincide_ultimo_dia(self):
        primer_dia = timezone.datetime(day=1, month=7, year=2023)
        ultimo_dia = timezone.datetime(day=31, month=12, year=2023)
        AnioAcademico.objects.create(fecha_inicio=primer_dia, fecha_fin=ultimo_dia)

        with self.assertRaises(ValidationError) as context:
            self.servicio_anio_academico.validar_anio_academico(
                fecha_inicio=timezone.datetime(day=1, month=1, year=2023),
                fecha_fin=primer_dia,
            )

        self.assertIn("fecha_inicio", context.exception.message_dict)
        self.assertIn("fecha_fin", context.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_inicio"),
        )
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_fin"),
        )

    def test_coincide_todo_el_periodo(self):
        primer_dia = timezone.datetime(day=1, month=7, year=2023)
        ultimo_dia = timezone.datetime(day=31, month=12, year=2023)
        AnioAcademico.objects.create(fecha_inicio=primer_dia, fecha_fin=ultimo_dia)

        with self.assertRaises(ValidationError) as context:
            self.servicio_anio_academico.validar_anio_academico(
                fecha_inicio=primer_dia,
                fecha_fin=ultimo_dia,
            )

        self.assertIn("fecha_inicio", context.exception.message_dict)
        self.assertIn("fecha_fin", context.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_inicio"),
        )
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_fin"),
        )

    def test_fecha_fin_antes_fecha_inicio(self):
        primer_dia = timezone.datetime(day=1, month=7, year=2023)
        ultimo_dia = timezone.datetime(day=31, month=12, year=2023)

        with self.assertRaises(ValidationError) as context:
            self.servicio_anio_academico.validar_anio_academico(
                fecha_inicio=ultimo_dia,
                fecha_fin=primer_dia,
            )

        self.assertIn("fecha_inicio", context.exception.message_dict)
        self.assertIn("fecha_fin", context.exception.message_dict)
        self.assertIn(
            MENSAJE_FECHAS_INCORRECTAS,
            context.exception.message_dict.get("fecha_inicio"),
        )
        self.assertIn(
            MENSAJE_FECHAS_INCORRECTAS,
            context.exception.message_dict.get("fecha_fin"),
        )

    def test_validar_fecha_de_anio_ya_existente(self):
        anio = AnioAcademico(
            fecha_inicio=timezone.datetime(day=1, month=7, year=2023),
            fecha_fin=timezone.datetime(day=31, month=12, year=2023),
        )

        self.servicio_anio_academico.validar_anio_academico(
            fecha_inicio=timezone.datetime(day=1, month=7, year=2023),
            fecha_fin=timezone.datetime(day=31, month=12, year=2023),
            instance=anio,
        )
