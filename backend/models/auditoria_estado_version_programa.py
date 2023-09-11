from django.db import models
from django.utils import timezone

from backend.common.choices import EstadoAsignatura

from .version_programa_asignatura import VersionProgramaAsignatura
from .rol import Rol


class AuditoriaEstadoVersionPrograma(models.Model):
    version_programa = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.CASCADE
    )
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    estado = models.CharField(max_length=2, choices=EstadoAsignatura.choices)
    modificado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Auditorias Estado Version Programas"
