from django.test import TestCase


class TestInformacionProgramaAPI(TestCase):
    def test_programa_no_aprobado(self):
        # Probar con todos los roles posibles que no vayan a tener permiso si esta desaprobado
        # - Docente de otra asignatura
        # - Director de carrera de una carrera que no tiene la asignatura
        pass

    def test_programa_aprobado(self):
        # Probar con cualquier tipo de rol y deberia enviar la informacion
        pass

    def test_usuario_no_autenticado(self):
        pass
