from django.db import models

from .asignatura import Asignatura


class PlanDeEstudio(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    version = models.TextField()
    nombre = models.TextField()

    # Foreign key
    carrera = models.ForeignKey("Carrera", on_delete=models.CASCADE)

    # Many to Many
    asignaturas = models.ManyToManyField(Asignatura)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="backend_plan_de_estudio_fecha_fin_posterior_a_fecha_inicio",
                check=models.Q(fecha_inicio__lte=models.F("fecha_fin")),
                violation_error_message="Fecha fin mayor o igual a fecha inicio.",  # Hacer archivo de constantes para mensajes de error
            )
        ]

    def __str__(self):
        return self.nombre
