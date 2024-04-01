from celery import shared_task

from backend.services.servicio_email import ServicioEmail
from backend.common.choices import TiposDeEmail

@shared_task()
def enviar_email_async(
    tipo: TiposDeEmail,
    destinatarios: list[str],
    subject: str,
    context:object
):
    servicio_email = ServicioEmail()
    servicio_email.enviar_email(
        tipo=tipo,
        destinatarios=destinatarios,
        subject=subject,
        context=context
    )