from django.db import models

from .estandar import Estandar
from backend.common.choices import TipoDescriptor


class Descriptor(models.Model):
    estandar = models.ForeignKey(Estandar, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(choices=TipoDescriptor.choices, max_length=1)

    def __str__(self):
        return "{} - {}".format(self.tipo, self.descripcion)

    class Meta:
        verbose_name_plural = "Descriptores"
