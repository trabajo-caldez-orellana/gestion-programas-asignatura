from django.db import models
from django.utils import timezone

from backend.common.choices import EstadoAsignatura
from .asignatura import Asignatura
from .semestre import Semestre


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
    recursos = models.TextField()
    evaluacion = models.TextField()
    investigacion_docentes = models.TextField()
    investigacion_estudiantes = models.TextField()
    extension_docentes = models.TextField()
    extension_estudiantes = models.TextField()
    cronograma = models.TextField()

    resultados_de_aprendizaje = models.JSONField()

    # TODO. cambiar a la funcio de fecha que cree en otro PR
    creado_en = models.DateTimeField(default=timezone.now)

    @property
    def carga_total(self) -> int:
        semanal_teoria_presencial = (
            0
            if self.ssemanal_teoria_presencial is None
            else self.semanal_teoria_presencial
        )
        semanal_practica_presencial = (
            0
            if self.semanal_practica_presencial is None
            else self.semanal_practica_presencial
        )
        semanal_teorico_practico_presencial = (
            0
            if self.semanal_teorico_practico_presencial is None
            else self.semanal_teorico_practico_presencial
        )
        semanal_lab_presencial = (
            0 if self.semanal_lab_presencial is None else self.semanal_lab_presencial
        )
        semanal_teoria_remoto = (
            0 if self.semanal_teoria_remoto is None else self.semanal_teoria_remoto
        )
        semanal_practica_remoto = (
            0 if self.semanal_practica_remoto is None else self.semanal_practica_remoto
        )
        semanal_teorico_practico_remoto = (
            0
            if self.semanal_teorico_practico_remoto is None
            else self.semanal_teorico_practico_remoto
        )
        semanal_lab_remoto = (
            0 if self.semanal_lab_remoto is None else self.semanal_lab_remoto
        )

        # TODO. Hay que multiplicar por las semanas de dicatdo? Hay que agregar las horas destinadas a evaluaciones?
        return (
            semanal_lab_presencial
            + semanal_lab_remoto
            + semanal_practica_presencial
            + semanal_practica_remoto
            + semanal_teoria_presencial
            + semanal_teoria_remoto
            + semanal_teorico_practico_presencial
            + semanal_teorico_practico_remoto
        )

    class Meta:
        verbose_name_plural = "Versiones de Programa de Asignatura"

    def str(self):
        return self.asignatura + "-" + self.semestre
