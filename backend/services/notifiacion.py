from backend.common.choices import TipoNotificacion
from backend.models import Usuario, Notificacion


class ServicioNotificacion:
    def _enviar_email(self, email: str, notifiacion: Notificacion):
        """
        Envia mail al usuario con la notificacion, y mensaje.
        """

        pass

    def crear_nueva_notificacion(
        self, usuario: Usuario, tipo: TipoNotificacion, mensaje: str, redirecciona: str
    ):
        """
        Crea una nueva notificacion. Envia mail al usuario con la notificacion.
        """

        pass
