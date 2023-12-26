from freezegun import freeze_time

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.common.mensajes_de_error import MENSAJE_NO_HAY_SEMESTRES_ANTERIORES
from backend.services import ServicioSemestre
from backend.common.choices import Semestres
from backend.models import Semestre
from backend.tests.utils import (
    crear_anios_de_prueba,
    crear_fecha_y_hora,
    FECHA_INICIO_ANIO_FUTURO,
    FECHA_FIN_ANIO_FUTURO,
    FECHA_INICIO_ANIO_ABIERTO,
    FECHA_FIN_ANIO_ABIERTO,
    FECHA_INICIO_ANIO_CERRADO,
    FECHA_FIN_ANIO_CERRADO,
)


class TestObtenerSemestreAnterior(TestCase):
    servicio_semestre = ServicioSemestre()

    def setUp(self) -> None:
        (
            self.anio_cerrado,
            self.anio_actual,
            self.anio_futuro,
        ) = crear_anios_de_prueba()

        # Creo dos semestres por anio. Anio Cerrado:
        dias_anio = FECHA_FIN_ANIO_CERRADO - FECHA_INICIO_ANIO_CERRADO
        self.primer_semestre_anio_cerrado = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_CERRADO,
            fecha_fin=(
                FECHA_INICIO_ANIO_CERRADO + timezone.timedelta(dias_anio.days / 2)
            ),
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_cerrado,
        )
        self.segundo_semestre_anio_cerrado = Semestre.objects.create(
            fecha_inicio=(
                FECHA_INICIO_ANIO_CERRADO + timezone.timedelta(dias_anio.days / 2 + 1)
            ),
            fecha_fin=FECHA_FIN_ANIO_CERRADO,
            semestre=Semestres.SEGUNDO,
            anio_academico=self.anio_cerrado,
        )

        # Creo dos semestres por anio. Anio abierto:
        dias_anio = FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO
        self.primer_semestre_anio_abierto = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=(
                FECHA_INICIO_ANIO_ABIERTO + timezone.timedelta(dias_anio.days / 2)
            ),
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_actual,
        )
        self.segundo_semestre_anio_abierto = Semestre.objects.create(
            fecha_inicio=(
                FECHA_INICIO_ANIO_ABIERTO + timezone.timedelta(dias_anio.days / 2 + 1)
            ),
            fecha_fin=FECHA_FIN_ANIO_ABIERTO,
            semestre=Semestres.SEGUNDO,
            anio_academico=self.anio_actual,
        )

        # Creo dos semestres por anio. Anio futuro:
        dias_anio = FECHA_FIN_ANIO_FUTURO - FECHA_INICIO_ANIO_FUTURO
        self.primer_semestre_anio_futuro = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_FUTURO,
            fecha_fin=FECHA_INICIO_ANIO_FUTURO + timezone.timedelta(dias_anio.days / 2),
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_futuro,
        )
        self.segundo_semestre_anio_futuro = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_FUTURO
            + timezone.timedelta(dias_anio.days / 2 + 1),
            fecha_fin=FECHA_FIN_ANIO_FUTURO,
            semestre=Semestres.SEGUNDO,
            anio_academico=self.anio_futuro,
        )

    def test_hay_mas_de_un_semestre_anterior(self):
        fecha_referencia = crear_fecha_y_hora(
            anio=FECHA_INICIO_ANIO_ABIERTO.year,
            mes=FECHA_INICIO_ANIO_ABIERTO.month,
            dia=FECHA_INICIO_ANIO_ABIERTO.day,
        )
        with freeze_time(fecha_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior()
            self.assertEqual(semestre, self.segundo_semestre_anio_cerrado)

    def test_probar_antes_de_media_noche_en_cambio_de_semestre(self):
        fecha_de_referencia = crear_fecha_y_hora(
            anio=FECHA_FIN_ANIO_CERRADO.year,
            mes=FECHA_FIN_ANIO_CERRADO.month,
            dia=FECHA_FIN_ANIO_CERRADO.day,
            hora=23,
            minuto=59,
            segundo=59,
        )
        with freeze_time(fecha_de_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior()

            self.assertEqual(semestre, self.primer_semestre_anio_cerrado)

    def test_probar_despues_de_media_noche_en_cambio_de_semestre(self):
        fecha_de_referencia = crear_fecha_y_hora(
            anio=FECHA_INICIO_ANIO_ABIERTO.year,
            mes=FECHA_INICIO_ANIO_ABIERTO.month,
            dia=FECHA_INICIO_ANIO_ABIERTO.day,
        )
        with freeze_time(fecha_de_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior()

        self.assertEqual(semestre, self.segundo_semestre_anio_cerrado)

    def test_no_se_crearon_semestres(self):
        Semestre.objects.all().delete()

        with self.assertRaises(ValidationError) as contexto:
            self.servicio_semestre.obtener_semestre_anterior()

        self.assertIn("__all__", contexto.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
            contexto.exception.message_dict["__all__"],
        )

    def test_no_hay_semestres_anteriores(self):
        fecha_de_referencia = crear_fecha_y_hora(
            dia=FECHA_INICIO_ANIO_CERRADO.day,
            mes=FECHA_INICIO_ANIO_CERRADO.month,
            anio=FECHA_INICIO_ANIO_CERRADO.year,
        )
        with freeze_time(fecha_de_referencia):
            with self.assertRaises(ValidationError) as contexto:
                self.servicio_semestre.obtener_semestre_anterior()

            self.assertIn("__all__", contexto.exception.message_dict)
            self.assertIn(
                MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
                contexto.exception.message_dict["__all__"],
            )

    def test_no_hay_semestre_actual(self):
        dia_despues_fin_anio_futuro = FECHA_FIN_ANIO_FUTURO + timezone.timedelta(days=1)
        fecha_referencia = crear_fecha_y_hora(
            dia=dia_despues_fin_anio_futuro.day,
            mes=dia_despues_fin_anio_futuro.month,
            anio=dia_despues_fin_anio_futuro.year,
        )
        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as contexto:
                self.servicio_semestre.obtener_semestre_anterior()

                self.assertIn("__all__", contexto.exception.message_dict)
                self.assertIn(
                    MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
                    contexto.exception.message_dict["__all__"],
                )

    def test_obtener_primer_semestre_anterior(self):
        # Primero pruebo cuando el semestre actual es del primer semestre
        fecha_de_referencia = crear_fecha_y_hora(
            FECHA_INICIO_ANIO_ABIERTO.year,
            FECHA_INICIO_ANIO_ABIERTO.month,
            FECHA_INICIO_ANIO_ABIERTO.day,
        )

        with freeze_time(fecha_de_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior(
                Semestres.PRIMER
            )
            self.assertEqual(semestre, self.primer_semestre_anio_cerrado)

        # Despues pruebo cuando el semestre actual es del segundo semestre
        ultimo_dia_anio_abierto = FECHA_FIN_ANIO_ABIERTO - timezone.timedelta(days=1)
        fecha_de_referencia = crear_fecha_y_hora(
            ultimo_dia_anio_abierto.year,
            ultimo_dia_anio_abierto.month,
            ultimo_dia_anio_abierto.day,
        )

        with freeze_time(fecha_de_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior(
                Semestres.PRIMER
            )
            self.assertEqual(semestre, self.primer_semestre_anio_abierto)

    def test_obtener_segundo_semestre_anterior(self):
        # Primero pruebo cuando el semestre actual es del primer semestre
        fecha_de_referencia = crear_fecha_y_hora(
            FECHA_INICIO_ANIO_ABIERTO.year,
            FECHA_INICIO_ANIO_ABIERTO.month,
            FECHA_INICIO_ANIO_ABIERTO.day,
        )

        with freeze_time(fecha_de_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior(
                Semestres.SEGUNDO
            )
            self.assertEqual(semestre, self.segundo_semestre_anio_cerrado)

        # Despues pruebo cuando el semestre actual es del segundo semestre
        ultimo_dia_anio_abierto = FECHA_FIN_ANIO_ABIERTO - timezone.timedelta(days=1)
        fecha_de_referencia = crear_fecha_y_hora(
            ultimo_dia_anio_abierto.year,
            ultimo_dia_anio_abierto.month,
            ultimo_dia_anio_abierto.day,
        )

        with freeze_time(fecha_de_referencia):
            semestre = self.servicio_semestre.obtener_semestre_anterior(
                Semestres.SEGUNDO
            )
            self.assertEqual(semestre, self.segundo_semestre_anio_cerrado)

    def test_no_hay_primer_semestre_anterior(self):
        fecha_de_referencia = crear_fecha_y_hora(
            FECHA_INICIO_ANIO_CERRADO.year,
            FECHA_INICIO_ANIO_CERRADO.month,
            FECHA_INICIO_ANIO_CERRADO.day,
        )

        with freeze_time(fecha_de_referencia):
            with self.assertRaises(ValidationError) as context:
                self.servicio_semestre.obtener_semestre_anterior(Semestres.PRIMER)

        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
            context.exception.message_dict["__all__"],
        )

    def test_no_hay_segundo_semestre_anterior(self):
        ultimo_dia_anio_cerrado = FECHA_FIN_ANIO_CERRADO - timezone.timedelta(days=1)
        fecha_de_referencia = crear_fecha_y_hora(
            ultimo_dia_anio_cerrado.year,
            ultimo_dia_anio_cerrado.month,
            ultimo_dia_anio_cerrado.day,
        )

        with freeze_time(fecha_de_referencia):
            with self.assertRaises(ValidationError) as context:
                self.servicio_semestre.obtener_semestre_anterior(Semestres.SEGUNDO)

        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
            context.exception.message_dict["__all__"],
        )

        ultimo_dia_anio_cerrado = FECHA_FIN_ANIO_CERRADO - timezone.timedelta(days=1)
        fecha_de_referencia = crear_fecha_y_hora(
            ultimo_dia_anio_cerrado.year,
            ultimo_dia_anio_cerrado.month,
            ultimo_dia_anio_cerrado.day,
        )

        with freeze_time(fecha_de_referencia):
            with self.assertRaises(ValidationError) as context:
                self.servicio_semestre.obtener_semestre_anterior(Semestres.SEGUNDO)

        self.assertIn(
            MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
            context.exception.message_dict["__all__"],
        )
