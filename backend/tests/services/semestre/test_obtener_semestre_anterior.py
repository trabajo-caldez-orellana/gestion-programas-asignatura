from django.test import TestCase

from backend.services import ServicioSemestre


class TestObtenerSemestreAnterior(TestCase):
    servicio_semestre = ServicioSemestre()

    def test_hay_semestre_actual_pero_no_anterior(self):
        pass

    def test_hay_dos_semestres_pasados_y_uno_actual(self):
        pass

    def test_no_hay_semestres_creados(self):
        pass
