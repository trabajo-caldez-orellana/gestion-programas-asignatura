import re

from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

from backend.common.choices import MetodologiaAsignatura
from backend.common.regular_expressions import CODIGO_ASIGANTURA_REGEXP
from backend.common.mensajes_de_error import CODIGO_ASIGNATURA_INCORRECTO
from .bloque_curricular import BloqueCurricular


class Asignatura(models.Model):
    denominacion = models.CharField(max_length=255)
    codigo = models.CharField(
        max_length=6, validators=[MinLengthValidator(6)], unique=True
    )
    metodologia = models.CharField(choices=MetodologiaAsignatura.choices, max_length=1)
    bloque_curricular = models.ForeignKey(BloqueCurricular, on_delete=models.PROTECT)

    def clean(self):
        if re.match(CODIGO_ASIGANTURA_REGEXP, self.codigo):
            raise ValidationError({"codigo": CODIGO_ASIGNATURA_INCORRECTO})

    def __str__(self):
        return "{} - {}".format(self.codigo, self.denominacion)
