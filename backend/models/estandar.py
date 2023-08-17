from django.db import models

from .carrera import Carrera


class Estandar(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
