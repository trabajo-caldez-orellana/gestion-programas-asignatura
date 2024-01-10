from django.test import TestCase


class TestAPIListarTareasPendientes(TestCase):
    def test_listar_usuario_no_autenticado(self):
        pass

    def test_listar_usuario_rol_secretario_academico(self):
        pass

    def test_listar_usuario_no_tiene_rol(self):
        pass

    def test_listar_docente_de_asignatura_de_otro_semestre(self):
        """El semestre siguiente no corresponde a un semestre en el que tenga cursado su asignatura"""
        pass

    def test_listar_docente_cumplio_con_todos_los_pendientes(self):
        pass

    def test_listar_docente_tiene_versiones_como_borrador(self):
        pass

    def test_listar_no_es_periodo_de_actualizacion_de_programas(self):
        pass

    def test_listar_docente_no_puede_reutilizar_porque_no_hay_version_anterior(self):
        pass

    def test_docente_puede_reutilizar_version_anterior(self):
        pass

    def test_director_de_carrera_es_tambien_docente(self):
        pass

    def test_director_de_carrera_debe_aprobar_cambios(self):
        pass

    def test_programas_todos_listos_para_el_semesstre_siguiente(self):
        """Probar que todo esta hecho a tiempo para todos los roles, y no quedan pendientes"""
        pass
