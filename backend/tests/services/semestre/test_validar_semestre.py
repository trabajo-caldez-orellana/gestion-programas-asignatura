from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import Semestre
from backend.common.choices import Semestres
from backend.services import ServicioSemestre
from backend.common.mensajes_de_error import (
    MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
    MENSAJE_FECHAS_INCORRECTAS,
)
from backend.tests.utils import (
    crear_anios_de_prueba,
    FECHA_INICIO_ANIO_ABIERTO,
    FECHA_FIN_ANIO_ABIERTO,
)


class TestValidarSemestre(TestCase):
    servicio_semestre = ServicioSemestre()

    def setUp(self) -> None:
        (
            self.anio_anterior,
            self.anio_actual,
            self.anio_siguiente,
        ) = crear_anios_de_prueba()

    def test_no_hay_semestres_creados(self):
        fecha_fin = (
            FECHA_INICIO_ANIO_ABIERTO
            + (FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO) / 2
        )
        self.servicio_semestre.validar_semestre(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            anio_academico=self.anio_actual,
            tipo_semestre=Semestres.PRIMER,
        )

    def test_coincide_primer_dia(self):
        fecha_fin = (
            FECHA_INICIO_ANIO_ABIERTO
            + (FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO) / 2
        )
        self.servicio_semestre.validar_semestre(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            anio_academico=self.anio_actual,
            tipo_semestre=Semestres.PRIMER,
        )

        Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_actual,
        )

        with self.assertRaises(ValidationError) as context:
            self.servicio_semestre.validar_semestre(
                fecha_inicio=fecha_fin,
                fecha_fin=FECHA_FIN_ANIO_ABIERTO,
                anio_academico=self.anio_actual,
                tipo_semestre=Semestres.SEGUNDO,
            )

        self.assertIn("fecha_inicio", context.exception.message_dict)
        self.assertIn("fecha_fin", context.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_inicio"),
        )
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_fin"),
        )

    def test_coincide_todo_el_periodo(self):
        fecha_fin = (
            FECHA_INICIO_ANIO_ABIERTO
            + (FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO) / 2
        )
        self.servicio_semestre.validar_semestre(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            anio_academico=self.anio_actual,
            tipo_semestre=Semestres.PRIMER,
        )

        Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_actual,
        )
        with self.assertRaises(ValidationError) as context:
            self.servicio_semestre.validar_semestre(
                fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
                fecha_fin=fecha_fin,
                anio_academico=self.anio_actual,
                tipo_semestre=Semestres.SEGUNDO,
            )

        self.assertIn("fecha_inicio", context.exception.message_dict)
        self.assertIn("fecha_fin", context.exception.message_dict)
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_inicio"),
        )
        self.assertIn(
            MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
            context.exception.message_dict.get("fecha_fin"),
        )

    def test_fecha_fin_antes_fecha_inicio(self):
        fecha_fin = (
            FECHA_INICIO_ANIO_ABIERTO
            + (FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO) / 2
        )

        with self.assertRaises(ValidationError) as context:
            self.servicio_semestre.validar_semestre(
                fecha_inicio=fecha_fin,
                fecha_fin=FECHA_INICIO_ANIO_ABIERTO,
                anio_academico=self.anio_actual,
                tipo_semestre=Semestres.PRIMER,
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

    def test_validar_fecha_de_semestre_ya_existente(self):
        fecha_fin = (
            FECHA_INICIO_ANIO_ABIERTO
            + (FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO) / 2
        )
        self.servicio_semestre.validar_semestre(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            anio_academico=self.anio_actual,
            tipo_semestre=Semestres.PRIMER,
        )

        semestre = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_actual,
        )

        self.servicio_semestre.validar_semestre(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=fecha_fin,
            anio_academico=self.anio_actual,
            tipo_semestre=Semestres.PRIMER,
            instance=semestre,
        )

    def test_validar_dos_primeros_semestres_en_el_anio(self):
        pass

    def test_validar_dos_segundos_semestres_en_el_anio(self):
        pass

    def test_validar_fecha_primer_semestre_fuera_del_anio(self):
        pass

    def test_validar_fecha_segundo_semestre_fuera_del_anio(self):
        pass

    def test_validar_segundo_semestre_antes_del_primero(self):
        pass
