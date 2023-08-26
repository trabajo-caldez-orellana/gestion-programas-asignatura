from django.db import models

from .estandar import Estandar


class ResultadoDeAprendizaje(models.Model):
    estandar = models.ForeignKey(Estandar, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
