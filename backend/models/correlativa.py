from django.db import models

from backend.common.choices import TipoCorrelativa
from .asignatura import Asignatura
from .version_programa_asignatura import VersionProgramaAsignatura


class Correlativa(models.Model):
    version_programa_asignatura = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.CASCADE
    )
    asignatura_correlativa = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TipoCorrelativa.choices)
