from typing import Any
from django.db import models
from django.utils import timezone

from .asignatura import Asignatura
from backend.common.mensajes_de_error import MENSAJE_FECHAS_INCORRECTAS


class ManagerPlanDeEstudio(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        """
        Crea un nuevo Plan de Estudio. Verificar que no haya ninguno vigente al momento de crearlo.
        """
        return super().create(**kwargs)


class PlanDeEstudio(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    version = models.TextField()
    nombre = models.TextField()

    carrera = models.ForeignKey("Carrera", on_delete=models.PROTECT)
    asignaturas = models.ManyToManyField(Asignatura)

    @property
    def esta_activo(self):
        return (
            self.fecha_fin is not None
            or self.fecha_fin >= timezone.now().astimezone().date()
        )

    class Meta:
        verbose_name_plural = "Planes de Estudio"
        constraints = [
            models.CheckConstraint(
                name="backend_plan_de_estudio_fecha_fin_posterior_a_fecha_inicio",
                check=models.Q(fecha_inicio__lte=models.F("fecha_fin")),
                violation_error_message=MENSAJE_FECHAS_INCORRECTAS,
            )
        ]

    objects = ManagerPlanDeEstudio()

    def __str__(self):
        return self.nombre
