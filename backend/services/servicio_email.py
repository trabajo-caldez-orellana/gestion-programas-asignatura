from mailersend import emails

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from backend.common.choices import TiposDeEmail

class ServicioEmail:
    def enviar_email(self, tipo: TiposDeEmail, destinatarios: list[str], subject: str, context: object):
        mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)
        mail_from = {"email": settings.MAILERSEND_FROM}
        destinatarios_array = [{"email": destinatario} for destinatario in destinatarios]

        mail_body = {}

        html = render_to_string(f"{tipo}.html", context=context)
        texto = strip_tags(html)
        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(destinatarios_array, mail_body)
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(html, mail_body)
        mailer.set_plaintext_content(texto, mail_body)

        mailer.send(mail_body)