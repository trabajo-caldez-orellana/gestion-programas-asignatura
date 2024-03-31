from django.db import models
from django.utils import timezone

from backend.common.choices import AccionesProgramaDeAsignatura
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual
from .version_programa_asignatura import VersionProgramaAsignatura
from .rol import Rol


class AuditoriaRevisionDocentes(models.Model):
    version_programa = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.CASCADE
    )
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    modificado_en = models.DateTimeField(default=obtener_fecha_y_hora_actual)
    accion = models.CharField(choices=AccionesProgramaDeAsignatura.choices, max_length=2)

    class Meta:
        verbose_name_plural = "Auditorias Revisión de Docentes"
