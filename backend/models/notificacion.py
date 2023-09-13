from django.db import models
from django.utils import timezone

from .usuario import Usuario


class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2)
    creada = models.DateTimeField(default=timezone.now)
    leida = models.DateTimeField(blank=None, null=None)
    mensaje = models.CharField(max_length=255, blank=True, null=True)

    # Link al cual redirecciona cuando se apreta la notificacion
    redirecciona = models.URLField(max_length=255)

    class Meta:
        verbose_name_plural = "Notificaciones"
