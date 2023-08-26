from django.db import models

from backend.common.choices import NivelDescriptor
from .descriptor import Descriptor
from .version_programa_asignatura import VersionProgramaAsignatura


class ProgramaTieneDescriptor(models.Model):
    descriptor = models.ForeignKey(Descriptor, on_delete=models.PROTECT)
    version_plan_asignatura = models.ForeignKey(
        VersionProgramaAsignatura, on_delete=models.CASCADE
    )
    nivel = models.IntegerField(choices=NivelDescriptor.choices)
