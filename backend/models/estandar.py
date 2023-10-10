from django.db import models

from .carrera import Carrera
from .descriptor import Descriptor


class Estandar(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    descriptores = models.ManyToManyField(Descriptor, blank=True, null=True)

    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Estándares"
