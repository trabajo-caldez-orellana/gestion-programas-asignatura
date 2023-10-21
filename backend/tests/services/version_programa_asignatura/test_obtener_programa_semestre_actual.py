from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.models import Asignatura, Carrera
from backend.services import ServicioVersionProgramaAsignatura, ServicioSemestre
from backend.tests.utils import (
    set_up_tests,
    crear_programa_de_asignatura,
    CODIGO_ASIGNATURA_1,
    CODIGO_ASIGNATURA_2,
    CARRERA_1,
    CARRERA_2,
)


class TestObtenerProgramaSemestreActual(TestCase):
    servicio_version_programa_asignatura = ServicioVersionProgramaAsignatura()
    servicio_semestre = ServicioSemestre()

    def setUp(self) -> None:
        set_up_tests()
        self.asignatura_1 = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_1)
        self.asignatura_2 = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_2)
        self.carrera_1 = Carrera.objects.get(nombre=CARRERA_1)
        self.carrera_2 = Carrera.objects.get(nombre=CARRERA_2)

    def test_no_hay_programas_en_el_semestre_actual(self):
        semeste_actual = self.servicio_semestre.obtener_semestre_actual()

        programa_actual = (
            self.servicio_version_programa_asignatura.obtener_programa_semestre_actual(
                asignatura=self.asignatura_1
            )
        )
        self.assertIsNone(programa_actual)

    def test_busca_programas_aprobados_y_no_hay(self):
        semeste_actual = self.servicio_semestre.obtener_semestre_actual()
        programa_no_aprobado = crear_programa_de_asignatura(
            asignatura=self.asignatura_1,
            semestre=semeste_actual,
            carrera=self.carrera_1,
            esta_aprobado=False,
        )

        programa_actual = (
            self.servicio_version_programa_asignatura.obtener_programa_semestre_actual(
                asignatura=self.asignatura_1, esta_aprobado=True
            )
        )
        self.assertIsNone(programa_actual)

    def test_busca_programas_aprobados_correctamente(self):
        semeste_actual = self.servicio_semestre.obtener_semestre_actual()
        programa_no_aprobado = crear_programa_de_asignatura(
            asignatura=self.asignatura_1,
            semestre=semeste_actual,
            carrera=self.carrera_1,
        )

        programa_actual = (
            self.servicio_version_programa_asignatura.obtener_programa_semestre_actual(
                asignatura=self.asignatura_1
            )
        )
        self.assertIsNotNone(programa_actual)

    def test_busca_programas_correctamente(self):
        semeste_actual = self.servicio_semestre.obtener_semestre_actual()
        programa_no_aprobado = crear_programa_de_asignatura(
            asignatura=self.asignatura_1,
            semestre=semeste_actual,
            carrera=self.carrera_1,
            esta_aprobado=False,
        )

        programa_actual = (
            self.servicio_version_programa_asignatura.obtener_programa_semestre_actual(
                asignatura=self.asignatura_1
            )
        )
        self.assertIsNotNone(programa_actual)
