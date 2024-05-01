import os
from celery import Celery

from django.conf import settings

from backend.tasks import enviar_email_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
app = Celery("backend", broker='redis://redis:6379')
app.conf.timezone = settings.TIME_ZONE

app.config_from_object("django.conf:settings", namespace="CELERY")
app.register_task(enviar_email_async)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
