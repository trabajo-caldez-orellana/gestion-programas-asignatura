from celery import shared_task

from backend.services.servicio_email import ServicioEmail
from backend.common.choices import TiposDeEmail


@shared_task
def enviar_email_async(
    tipo: TiposDeEmail, destinatarios: list[str], subject: str, context: object
):
    servicio_email = ServicioEmail()

    # Se que no es lo mejor hacer con un loop, pero por el plan que tengo de mailersend no puedo enviar
    # una lista de destinatarios.
    for destinatario in destinatarios:
        servicio_email.enviar_email(
            tipo=tipo, destinatarios=[destinatario], subject=subject, context=context
        )
