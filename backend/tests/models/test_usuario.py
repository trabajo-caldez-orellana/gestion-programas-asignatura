from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.models import Usuario
from backend.common.mensajes_de_error import (
    MENSAJE_EMAIL_NO_PROPORCIONADO,
    MENSAJE_SUPERUSUARIO_ACTIVO,
    MENSAJE_SUPERUSUARIO_STAFF,
    MENSAJE_SUPERUSUARIO,
)


class TestUsuario(TestCase):
    # Testeo de las propiedades del modelo de notificacion
    def test_email_faltante(self):
        with self.assertRaises(ValidationError) as context:
            usuario = Usuario.objects.create_user(email=None, password="Pass.1234")

        self.assertIn(
            MENSAJE_EMAIL_NO_PROPORCIONADO, context.exception.message_dict["email"]
        )

        with self.assertRaises(ValidationError) as context:
            usuario = Usuario.objects.create_user(email="", password="Pass.1234")

        self.assertIn(
            MENSAJE_EMAIL_NO_PROPORCIONADO, context.exception.message_dict["email"]
        )

    def test_crear_superusuario(self):
        Usuario.objects.create_superuser("email@mail.com", "Password")

    def test_crear_superusuario_inactivo(self):
        with self.assertRaises(ValidationError) as context:
            Usuario.objects.create_superuser(
                email="email@mail.com", password="Password", is_active=False
            )
        self.assertIn(
            MENSAJE_SUPERUSUARIO_ACTIVO, context.exception.message_dict["is_active"]
        )

    def test_crear_superusuario_no_staff(self):
        with self.assertRaises(ValidationError) as context:
            Usuario.objects.create_superuser(
                email="email@mail.com", password="Password", is_staff=False
            )
        self.assertIn(
            MENSAJE_SUPERUSUARIO_STAFF, context.exception.message_dict["is_staff"]
        )

    def test_crear_superusuario_con_indicadir_de_superusuario_en_falso(self):
        with self.assertRaises(ValidationError) as context:
            Usuario.objects.create_superuser(
                email="email@mail.com", password="Password", is_superuser=False
            )
        self.assertIn(
            MENSAJE_SUPERUSUARIO, context.exception.message_dict["is_superuser"]
        )
