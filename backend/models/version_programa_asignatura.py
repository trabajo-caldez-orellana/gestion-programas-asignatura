from django.db import models

from backend.common.choices import EstadoAsignatura
from .asignatura import Asignatura
from .semestre import Semestre
from .resultado_de_aprendizaje import ResultadoDeAprendizaje


class VersionProgramaAsignatura(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=2, choices=EstadoAsignatura.choices, default=EstadoAsignatura.ABIERTO
    )
    semanas_dictado = models.PositiveIntegerField()
    semanal_teoria_presencial = models.PositiveIntegerField(blank=True, null=True)
    semanal_practica_presencial = models.PositiveIntegerField(blank=True, null=True)
    semanal_teorico_practico_presencial = models.PositiveIntegerField(
        blank=True, null=True
    )
    semanal_lab_presencial = models.PositiveIntegerField(blank=True, null=True)
    semanal_teoria_remoto = models.PositiveIntegerField(blank=True, null=True)
    semanal_practica_remoto = models.PositiveIntegerField(blank=True, null=True)
    semanal_teorico_practico_remoto = models.PositiveIntegerField(blank=True, null=True)
    semanal_lab_remoto = models.PositiveIntegerField(blank=True, null=True)
    contenidos = models.TextField()
    bibliografia = models.TextField()
    metodologia = models.TextField()
    recursos = models.TextField()
    evaluacion = models.TextField()
    investigacion_docentes = models.TextField()
    investigacion_estudiantes = models.TextField()
    extension_docentes = models.TextField()
    extension_estudiantes = models.TextField()
    cronograma = models.TextField()

    resultados_de_aprendizaje = models.ManyToManyField(ResultadoDeAprendizaje)
