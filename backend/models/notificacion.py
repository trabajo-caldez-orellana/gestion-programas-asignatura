from django.db import models
from django.utils import timezone

from .usuario import Usuario
from backend.common.choices import TipoNotificacion
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual


class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TipoNotificacion.choices)
    creada = models.DateTimeField(default=obtener_fecha_y_hora_actual)
    leida = models.DateTimeField(blank=True, null=True)
    mensaje = models.CharField(max_length=255, blank=True, null=True)

    # Link al cual redirecciona cuando se apreta la notificacion
    redirecciona = models.URLField(max_length=255)

    class Meta:
        verbose_name_plural = "Notificaciones"

    @property
    def fue_leida(self):
        return self.leida is not None
