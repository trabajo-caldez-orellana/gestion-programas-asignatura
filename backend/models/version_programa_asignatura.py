from django.db import models

from backend.common.choices import EstadoAsignatura
from .asignatura import Asignatura
from .semestre import Semestre


class VersionProgramaAsignatura(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=2, choices=EstadoAsignatura.choices, default=EstadoAsignatura.ABIERTO
    )
    resultados_aprendizaje = models.JSONField()
    semanas_dictado = models.IntegerField()
    semanal_teoria_presencial = models.IntegerField(blank=True, null=True)
    semanal_practica_presencial = models.IntegerField(blank=True, null=True)
    semanal_teorico_practico_presencial = models.IntegerField(blank=True, null=True)
    semanal_lab_presencial = models.IntegerField(blank=True, null=True)
    semanal_teoria_remoto = models.IntegerField(blank=True, null=True)
    semanal_practica_remoto = models.IntegerField(blank=True, null=True)
    semanal_teorico_practico_remoto = models.IntegerField(blank=True, null=True)
    semanal_lab_remoto = models.IntegerField(blank=True, null=True)
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
