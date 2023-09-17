from django.db import models

from .estandar import Estandar


class ActividadReservada(models.Model):
    estandar = models.ForeignKey(Estandar, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Actividades Reservadas"
