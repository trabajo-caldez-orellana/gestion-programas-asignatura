from django.test import TestCase
from django.core.exceptions import ValidationError


from backend.models import Asignatura, BloqueCurricular
from backend.common.choices import MetodologiaAsignatura
from backend.common.mensajes_de_error import (
    MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
    MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
    CODIGO_ASIGNATURA_INCORRECTO,
)


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
            codigo="15_PPP",
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
            codigo="15_PPV",
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
            codigo="15_PPH",
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
            codigo="15_PPP",
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

    def test_crear_asignatura_con_carga_bloqueada(self):
        # Para asignatura presencial
        campos_bloqueados = [
            "semanal_teoria_remoto",
            "semanal_practica_remoto",
            "semanal_teorico_practico_remoto",
            "semanal_lab_remoto",
        ]

        datos_default = {
            "denominacion": "Asignatura Prueba",
            "codigo": "15_PPP",
            "metodologia": MetodologiaAsignatura.PRESENCIAL,
            "bloque_curricular": self.bloque_curricular,
            "semanas_dictado": 16,
            "semanal_teoria_presencial": 2,
            "semanal_practica_presencial": 2,
            "semanal_teorico_practico_presencial": 2,
            "semanal_lab_presencial": 2,
            "carga_rtf": 20,
        }

        for campo in campos_bloqueados:
            datos = {**datos_default}
            datos[campo] = 2

            with self.assertRaises(ValidationError) as context:
                Asignatura.objects.create(**datos)

            self.assertIn(
                MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
                context.exception.message_dict[campo],
            )

        # Para asignatura virtual
        campos_bloqueados = [
            "semanal_teoria_presencial",
            "semanal_practica_presencial",
            "semanal_teorico_practico_presencial",
            "semanal_lab_presencial",
        ]

        datos_default = {
            "denominacion": "Asignatura Prueba",
            "codigo": "15_PPP",
            "metodologia": MetodologiaAsignatura.VIRTUAL,
            "bloque_curricular": self.bloque_curricular,
            "semanas_dictado": 16,
            "semanal_teoria_remoto": 2,
            "semanal_practica_remoto": 2,
            "semanal_teorico_practico_remoto": 2,
            "semanal_lab_remoto": 2,
            "carga_rtf": 20,
        }

        for campo in campos_bloqueados:
            datos = {**datos_default}
            datos[campo] = 2

            with self.assertRaises(ValidationError) as context:
                Asignatura.objects.create(**datos)

            self.assertIn(
                MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
                context.exception.message_dict[campo],
            )

    def test_crear_asignatura_con_carga_faltante(self):
        # Para asignatura presencial
        campos_necesarios = [
            "semanal_teoria_presencial",
            "semanal_practica_presencial",
            "semanal_teorico_practico_presencial",
            "semanal_lab_presencial",
        ]

        datos_default = {
            "denominacion": "Asignatura Prueba",
            "codigo": "15_PPP",
            "metodologia": MetodologiaAsignatura.PRESENCIAL,
            "bloque_curricular": self.bloque_curricular,
            "semanas_dictado": 16,
            "semanal_teoria_presencial": 2,
            "semanal_practica_presencial": 2,
            "semanal_teorico_practico_presencial": 2,
            "semanal_lab_presencial": 2,
            "carga_rtf": 20,
        }

        for campo in campos_necesarios:
            datos = {**datos_default}
            datos.pop(campo)

            with self.assertRaises(ValidationError) as context:
                Asignatura.objects.create(**datos)

            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                context.exception.message_dict[campo],
            )

        # Para asignatura virtual
        campos_necesarios = [
            "semanal_teoria_remoto",
            "semanal_practica_remoto",
            "semanal_teorico_practico_remoto",
            "semanal_lab_remoto",
        ]

        datos_default = {
            "denominacion": "Asignatura Prueba",
            "codigo": "15_PPP",
            "metodologia": MetodologiaAsignatura.VIRTUAL,
            "bloque_curricular": self.bloque_curricular,
            "semanas_dictado": 16,
            "semanal_teoria_remoto": 2,
            "semanal_practica_remoto": 2,
            "semanal_teorico_practico_remoto": 2,
            "semanal_lab_remoto": 2,
            "carga_rtf": 20,
        }

        for campo in campos_necesarios:
            datos = {**datos_default}
            datos.pop(campo)

            with self.assertRaises(ValidationError) as context:
                Asignatura.objects.create(**datos)

            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                context.exception.message_dict[campo],
            )

        # Para asignatura hibrido
        campos_necesarios = [
            "semanal_teoria_remoto",
            "semanal_practica_remoto",
            "semanal_teorico_practico_remoto",
            "semanal_lab_remoto",
            "semanal_teoria_presencial",
            "semanal_practica_presencial",
            "semanal_teorico_practico_presencial",
            "semanal_lab_presencial",
        ]

        datos_default = {
            "denominacion": "Asignatura Prueba",
            "codigo": "15_PPP",
            "metodologia": MetodologiaAsignatura.HIBRIDO,
            "bloque_curricular": self.bloque_curricular,
            "semanas_dictado": 16,
            "semanal_teoria_remoto": 2,
            "semanal_practica_remoto": 2,
            "semanal_teorico_practico_remoto": 2,
            "semanal_lab_remoto": 2,
            "semanal_teoria_presencial": 2,
            "semanal_practica_presencial": 2,
            "semanal_teorico_practico_presencial": 2,
            "semanal_lab_presencial": 2,
            "carga_rtf": 20,
        }

        for campo in campos_necesarios:
            datos = {**datos_default}
            datos.pop(campo)

            with self.assertRaises(ValidationError) as context:
                Asignatura.objects.create(**datos)

            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                context.exception.message_dict[campo],
            )

    def test_crear_asignatura_con_codigos_invalidos(self):
        codigos_invalidos = [
            "15_ABCD",
            "15_AB",
            "16_ABC",
            "15_abc",
            "15_123",
            "15_",
            "15_ABCDE",
            "14_ABC",
        ]

        datos_default = {
            "denominacion": "Asignatura Prueba",
            "metodologia": MetodologiaAsignatura.VIRTUAL,
            "bloque_curricular": self.bloque_curricular,
            "semanas_dictado": 16,
            "semanal_teoria_remoto": 2,
            "semanal_practica_remoto": 2,
            "semanal_teorico_practico_remoto": 2,
            "semanal_lab_remoto": 2,
            "carga_rtf": 20,
        }

        for codigo in codigos_invalidos:
            datos_default["codigo"] = codigo
            with self.assertRaises(ValidationError) as context:
                Asignatura.objects.create(**datos_default)

            self.assertIn(
                CODIGO_ASIGNATURA_INCORRECTO,
                context.exception.message_dict["codigo"],
            )
