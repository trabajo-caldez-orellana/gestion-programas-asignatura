from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.models import Usuario
from backend.common.mensajes_de_error import MENSAJE_EMAIL_NO_PROPORCIONADO


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

    def test_contrasenia_invalida(self):
        pass

    """  def test_notificacion_no_leida(self):
        self.assertFalse(self.notificacion.fue_leida)

    def test_carga_total(self):
        self.notificacion.leida = obtener_fecha_y_hora_actual()
        self.notificacion.full_clean()
        self.notificacion.save()
        self.assertTrue(self.notificacion.fue_leida) """
