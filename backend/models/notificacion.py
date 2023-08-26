from django.db import models
from django.utils import timezone


class Notificacion(models.Model):
    # TODO. Falta usuario para la notificacion
    tipo = models.CharField(max_length=2)
    creada = models.DateTimeField(default=timezone.now)
    leida = models.DateTimeField(blank=None, null=None)
