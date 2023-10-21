from django.test import TestCase

from backend.services import ServicioSemestre


class TestObtenerSemestreActual(TestCase):
    servicio_semestre = ServicioSemestre()

    def setUp(self) -> None:
        return super().setUp()

    def test_hay_un_semestre_pasado_y_no_uno_actual(self):
        pass

    def test_semestres_se_solapan(self):
        pass
