from django.test import TestCase

from backend.models import Asignatura, BloqueCurricular
from backend.common.choices import MetodologiaAsignatura


class TestAsignatura(TestCase):
    # Testeo de las propiedades del modelo de asignaturas
    def setUp(self) -> None:
        self.bloque_curricular = BloqueCurricular.objects.create(
            nombre="Bloque Curricular Prueba", coeficiente=1
        )

    def test_horas_semanales_clases(self):
        carga_teoria = 4
        carga_practica = 2
        carga_teorico_practico = 2
        carga_lab = 0
        carga_esperada = (
            carga_teoria + carga_practica + carga_teorico_practico + carga_lab
        )

        # Primero pruebo para metodologia presencial
        asignatura = Asignatura.objects.create(
            denominacion="Asignatura Prueba",
            codigo="15_PP1",
            metodologia=MetodologiaAsignatura.PRESENCIAL,
            bloque_curricular=self.bloque_curricular,
            semanas_dictado=16,
            semanal_teoria_presencial=carga_teoria,
            semanal_practica_presencial=carga_practica,
            semanal_teorico_practico_presencial=carga_teorico_practico,
            semanal_lab_presencial=carga_lab,
            carga_rtf=10,
        )

        self.assertEqual(asignatura.horas_semanales_clases, carga_esperada)

        # Pruebo para metodologia virtual
        asignatura = Asignatura.objects.create(
            denominacion="Asignatura Prueba",
            codigo="15_PP2",
            metodologia=MetodologiaAsignatura.VIRTUAL,
            bloque_curricular=self.bloque_curricular,
            semanas_dictado=16,
            semanal_teoria_remoto=carga_teoria,
            semanal_practica_remoto=carga_practica,
            semanal_teorico_practico_remoto=carga_teorico_practico,
            semanal_lab_remoto=carga_lab,
            carga_rtf=10,
        )

        self.assertEqual(asignatura.horas_semanales_clases, carga_esperada)

        # Pruebo para metodologia hibrida
        asignatura = Asignatura.objects.create(
            denominacion="Asignatura Prueba",
            codigo="15_PP3",
            metodologia=MetodologiaAsignatura.HIBRIDO,
            bloque_curricular=self.bloque_curricular,
            semanas_dictado=16,
            semanal_teoria_remoto=carga_teoria,
            semanal_practica_remoto=carga_practica,
            semanal_teorico_practico_remoto=carga_teorico_practico,
            semanal_lab_remoto=carga_lab,
            semanal_teoria_presencial=carga_teoria,
            semanal_practica_presencial=carga_practica,
            semanal_teorico_practico_presencial=carga_teorico_practico,
            semanal_lab_presencial=carga_lab,
            carga_rtf=10,
        )

        self.assertEqual(asignatura.horas_semanales_clases, carga_esperada * 2)

    def test_carga_total(self):
        carga_teoria = 4
        carga_practica = 2
        carga_teorico_practico = 2
        carga_lab = 0
        semanas_dictado = 16
        carga_esperada = (
            carga_teoria + carga_practica + carga_teorico_practico + carga_lab
        ) * semanas_dictado

        asignatura = Asignatura.objects.create(
            denominacion="Asignatura Prueba",
            codigo="15_PP1",
            metodologia=MetodologiaAsignatura.PRESENCIAL,
            bloque_curricular=self.bloque_curricular,
            semanas_dictado=semanas_dictado,
            semanal_teoria_presencial=carga_teoria,
            semanal_practica_presencial=carga_practica,
            semanal_teorico_practico_presencial=carga_teorico_practico,
            semanal_lab_presencial=carga_lab,
            carga_rtf=10,
        )

        self.assertEqual(carga_esperada, asignatura.carga_total)
