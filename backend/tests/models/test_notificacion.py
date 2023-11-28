from django.test import TestCase

from backend.models import Notificacion, Usuario
from backend.common.choices import TipoNotificacion
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual


class TestNotificacion(TestCase):
    # Testeo de las propiedades del modelo de notificacion
    def setUp(self) -> None:
        self.usuario = Usuario.objects.create_user(
            email="test_user@mail.com", password="Pass.1234"
        )
        self.notificacion = Notificacion.objects.create(
            usuario=self.usuario,
            tipo=TipoNotificacion.VERSION_PENDIENTE,
            redirecciona="http://fakeurl.com",
        )

    def test_notificacion_no_leida(self):
        self.assertFalse(self.notificacion.fue_leida)

    def test_carga_total(self):
        self.notificacion.leida = obtener_fecha_y_hora_actual()
        self.notificacion.full_clean()
        self.notificacion.save()
        self.assertTrue(self.notificacion.fue_leida)
