import os
from celery import Celery

from django.conf import settings
from backend.tasks import enviar_email_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
app = Celery("backend", broker='redis://redis:6379/0')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.register_task(enviar_email_async)
app.conf.timezone = settings.TIME_ZONE
app.task(enviar_email_async)
