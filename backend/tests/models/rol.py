from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.models import Usuario, Rol, Carrera, Asignatura
from backend.common.choices import Roles
from backend.tests.utils import set_up_tests, CODIGO_ASIGNATURA_1, CARRERA_1
from backend.common.mensajes_de_error import (
    MENSAJE_DOCENTE_SELECCIONA_ASIGNATURA,
    MENSAJE_DOCENTE_SELECCIONA_CARRERA,
    MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA,
    MENSAJE_DIRECTOR_SELECCIONA_ASIGNATURA,
    MENSAJE_DIRECTOR_SELECCIONA_CARRERA,
)


class TestRol(TestCase):
    # Testeo de las propiedades del modelo de notificacion
    def setUp(self) -> None:
        set_up_tests()
        self.carrera = Carrera.objects.get(nombre=CARRERA_1)
        self.asignatura = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_1)
        self.usuario = Usuario.objects.create_user(
            email="test_user@mail.com", password="Pass.1234"
        )

    def test_rol_docente_falta_asignatura(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(usuario=self.usuario, rol=Roles.DOCENTE)

        self.assertIn(
            MENSAJE_DOCENTE_SELECCIONA_ASIGNATURA,
            context.exception.message_dict["asignatura"],
        )

    def test_rol_titular_catedra_falta_asignatura(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(usuario=self.usuario, rol=Roles.TITULAR_CATEDRA)

        self.assertIn(
            MENSAJE_DOCENTE_SELECCIONA_ASIGNATURA,
            context.exception.message_dict["asignatura"],
        )

    def test_rol_docente_tiene_carrera(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(
                usuario=self.usuario,
                rol=Roles.DOCENTE,
                asignatura=self.asignatura,
                carrera=self.carrera,
            )

        self.assertIn(
            MENSAJE_DOCENTE_SELECCIONA_CARRERA,
            context.exception.message_dict["carrera"],
        )

    def test_rol_titular_catedra_tiene_carrera(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(
                usuario=self.usuario,
                rol=Roles.DOCENTE,
                asignatura=self.asignatura,
                carrera=self.carrera,
            )

        self.assertIn(
            MENSAJE_DOCENTE_SELECCIONA_CARRERA,
            context.exception.message_dict["carrera"],
        )

    def test_rol_director_carrera_falta_carrera(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(usuario=self.usuario, rol=Roles.DIRECTOR_CARRERA)

        self.assertIn(
            MENSAJE_DIRECTOR_SELECCIONA_CARRERA,
            context.exception.message_dict["carrera"],
        )

    def test_rol_director_carrera_tiene_asignatura(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(
                usuario=self.usuario,
                rol=Roles.DIRECTOR_CARRERA,
                asignatura=self.asignatura,
                carrera=self.carrera,
            )

        self.assertIn(
            MENSAJE_DIRECTOR_SELECCIONA_ASIGNATURA,
            context.exception.message_dict["asignatura"],
        )

    def test_rol_secretario_academico_tiene_carrera(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(
                usuario=self.usuario,
                rol=Roles.SECRETARIO,
                carrera=self.carrera,
            )

        self.assertIn(
            MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA,
            context.exception.message_dict["carrera"],
        )

    def test_rol_secretario_academico_tiene_asignatura(self):
        with self.assertRaises(ValidationError) as context:
            Rol.objects.create(
                usuario=self.usuario,
                rol=Roles.SECRETARIO,
                asignatura=self.asignatura,
            )

        self.assertIn(
            MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA,
            context.exception.message_dict["asignatura"],
        )

    def test_crear_rol_docente_correctamente(self):
        Rol.objects.create(
            usuario=self.usuario,
            rol=Roles.DOCENTE,
            asignatura=self.asignatura,
        )

    def test_crear_rol_titular_catedra_correctamente(self):
        Rol.objects.create(
            usuario=self.usuario,
            rol=Roles.TITULAR_CATEDRA,
            asignatura=self.asignatura,
        )

    def test_crear_rol_secretario_academico_correctamente(self):
        Rol.objects.create(
            usuario=self.usuario,
            rol=Roles.SECRETARIO,
        )

    def test_crear_rol_director_carrera_correctamente(self):
        Rol.objects.create(
            usuario=self.usuario,
            rol=Roles.DIRECTOR_CARRERA,
            carrera=self.carrera,
        )
