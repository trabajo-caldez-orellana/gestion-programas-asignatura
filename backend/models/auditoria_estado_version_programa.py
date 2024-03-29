from django.db import models
from django.utils import timezone

from backend.common.choices import EstadosAprobacionPrograma

from .version_programa_asignatura import VersionProgramaAsignatura
from .rol import Rol


class AuditoriaEstadoVersionPrograma(models.Model):
    version_programa = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.CASCADE
    )
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    estado = models.CharField(max_length=2, choices=EstadosAprobacionPrograma.choices)
    modificado_en = models.DateTimeField(default=timezone.now)
    mensaje_cambios = models.TextField()

    class Meta:
        verbose_name_plural = "Auditorias Estado Version Programas"
