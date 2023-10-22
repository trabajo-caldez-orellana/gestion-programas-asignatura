from django.db import models
from django.utils import timezone

from backend.common.mensajes_de_error import MENSAJE_FECHAS_INCORRECTAS


class Semestre(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="backend_semestre_fecha_fin_posterior_a_fecha_inicio",
                check=models.Q(fecha_inicio__lte=models.F("fecha_fin")),
                violation_error_message=MENSAJE_FECHAS_INCORRECTAS,
            )
        ]

    @property
    def esta_activo(self) -> bool:
        hoy = timezone.now().astimezone().date()

        return self.fecha_inicio <= hoy <= self.fecha_fin

    def __str__(self):
        return "Semestre {} - {}".format(self.fecha_inicio, self.fecha_fin)
