from django.db import models

from backend.common.choices import TipoCorrelativa, RequisitosCorrelativa
from .asignatura import Asignatura
from .version_programa_asignatura import VersionProgramaAsignatura


class Correlativa(models.Model):
    version_programa_asignatura = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.PROTECT
    )
    asignatura_correlativa = models.ForeignKey(
        Asignatura, on_delete=models.PROTECT, blank=True, null=True
    )
    tipo = models.CharField(max_length=1, choices=TipoCorrelativa.choices)
    requisito = models.CharField(max_length=10, choices=RequisitosCorrelativa.choices)
    modulo = models.CharField(max_length=255, blank=True, null=True)
    cantidad_asignaturas = models.PositiveIntegerField(blank=True, null=True)
