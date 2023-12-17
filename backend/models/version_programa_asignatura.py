from django.db import models

from backend.common.choices import EstadoAsignatura
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual
from .asignatura import Asignatura
from .semestre import Semestre


class VersionProgramaAsignatura(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=2, choices=EstadoAsignatura.choices, default=EstadoAsignatura.ABIERTO
    )
    contenidos = models.TextField()
    bibliografia = models.TextField()
    recursos = models.TextField()
    evaluacion = models.TextField()
    investigacion_docentes = models.TextField()
    investigacion_estudiantes = models.TextField()
    extension_docentes = models.TextField()
    extension_estudiantes = models.TextField()
    cronograma = models.TextField()

    resultados_de_aprendizaje = models.JSONField()
    creado_en = models.DateTimeField(default=obtener_fecha_y_hora_actual)

    class Meta:
        verbose_name_plural = "Versiones de Programa de Asignatura"

    def __str__(self):
        return self.asignatura + "-" + self.semestre
