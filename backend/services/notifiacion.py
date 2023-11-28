from backend.common.choices import TipoNotificacion  # pragma: no cover
from backend.models import Usuario, Notificacion  # pragma: no cover

# TODO. sacar el no cover cuando haga estos servicios


class ServicioNotificacion:  # pragma: no cover
    def _enviar_email(self, email: str, notifiacion: Notificacion):  # pragma: no cover
        """
        Envia mail al usuario con la notificacion, y mensaje.
        """

        pass

    def crear_nueva_notificacion(
        self, usuario: Usuario, tipo: TipoNotificacion, mensaje: str, redirecciona: str
    ):  # pragma: no cover
        """
        Crea una nueva notificacion. Envia mail al usuario con la notificacion.
        """

        pass
