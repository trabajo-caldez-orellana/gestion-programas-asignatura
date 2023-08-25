from django.db import models
from django.core.validators import MinLengthValidator

from backend.common.choices import MetodologiaAsignatura
from .bloque_curricular import BloqueCurricular


class Asignatura(models.Model):
    denominacion = models.CharField(max_length=255)
    codigo = models.CharField(
        max_length=6, validators=[MinLengthValidator(6)], unique=True
    )
    metodologia = models.CharField(choices=MetodologiaAsignatura.choices, max_length=1)
    bloque_curricular = models.ForeignKey(BloqueCurricular, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.denominacion)
