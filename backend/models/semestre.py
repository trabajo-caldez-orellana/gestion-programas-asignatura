from django.db import models
from django.utils import timezone

from backend.common.mensajes_de_error import MENSAJE_FECHAS_INCORRECTAS
from backend.models.anio_academico import AnioAcademico
from backend.common.choices import Semestres
from backend.common.funciones_fecha import obtener_fecha_actual


class Semestre(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    anio_academico = models.ForeignKey(AnioAcademico, on_delete=models.PROTECT)
    semestre = models.CharField(max_length=2, choices=Semestres.choices)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="backend_semestre_fecha_fin_posterior_a_fecha_inicio",
                check=models.Q(fecha_inicio__lte=models.F("fecha_fin")),
                violation_error_message=MENSAJE_FECHAS_INCORRECTAS,
            ),
            models.UniqueConstraint(
                fields=["anio_academico", "semestre"],
                name="backend_semestre_un_semestre_de_tipo_por_anio_academico",
            ),
        ]

    @property
    def esta_activo(self) -> bool:
        hoy = obtener_fecha_actual()
        return self.fecha_inicio <= hoy <= self.fecha_fin

    def __str__(self):
        return "{} - {}".format(self.get_semestre_display(), str(self.anio_academico))
