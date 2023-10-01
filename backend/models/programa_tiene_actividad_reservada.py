from django.db import models

from backend.common.choices import NivelDescriptor
from .actividad_reservada import ActividadReservada
from .version_programa_asignatura import VersionProgramaAsignatura


class ProgramaTieneActividadReservada(models.Model):
    actividad_reservada = models.ForeignKey(
        ActividadReservada, on_delete=models.PROTECT
    )
    version_plan_asignatura = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.CASCADE
    )
    nivel = models.IntegerField(choices=NivelDescriptor.choices)

    class Meta:
        verbose_name_plural = "Actividades Reservadas para Programas"
