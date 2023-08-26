from django.db import models

from .asignatura import Asignatura
from backend.common.mensajes_de_error import MENSAJE_FECHAS_INCORRECTAS


class PlanDeEstudio(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    version = models.TextField()
    nombre = models.TextField()

    carrera = models.ForeignKey("Carrera", on_delete=models.PROTECT)
    asignaturas = models.ManyToManyField(Asignatura)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="backend_plan_de_estudio_fecha_fin_posterior_a_fecha_inicio",
                check=models.Q(fecha_inicio__lte=models.F("fecha_fin")),
                violation_error_message=MENSAJE_FECHAS_INCORRECTAS,
            )
        ]

    def __str__(self):
        return self.nombre
