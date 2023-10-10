from django.contrib import admin

from backend.models import (
    ProgramaTieneDescriptor,
    ProgramaTieneActividadReservada,
    Correlativa,
    CargaBloque,
)


class DescriptorInline(admin.TabularInline):
    model = ProgramaTieneDescriptor


class ActividadReservadaInline(admin.TabularInline):
    model = ProgramaTieneActividadReservada


class CargaBloqueInline(admin.TabularInline):
    model = CargaBloque


class CorrelativaInline(admin.TabularInline):
    model = Correlativa


class AdminVersionProgramaAsignatura(admin.ModelAdmin):
    list_display = ["asignatura", "semestre", "estado"]
    inlines = [
        DescriptorInline,
        ActividadReservadaInline,
        CargaBloqueInline,
        CorrelativaInline,
    ]

    fieldsets = [
        (
            None,
            {"fields": ["asignatura", "semestre", "estado"]},
        ),
        (
            "Horas Semanales",
            {
                "classes": ["extrapretty"],
                "fields": [
                    "semanas_dictado",
                    "semanal_teoria_presencial",
                    "semanal_practica_presencial",
                    "semanal_teorico_practico_presencial",
                    "semanal_lab_presencial",
                    "semanal_teoria_remoto",
                    "semanal_practica_remoto",
                    "semanal_teorico_practico_remoto",
                    "semanal_lab_remoto",
                ],
            },
        ),
        (
            "Informacion del Cursado",
            {
                "fields": [
                    "contenidos",
                    "bibliografia",
                    "metodologia",
                    "recursos",
                    "evaluacion",
                    "cronograma",
                    "resultados_de_aprendizaje",
                ]
            },
        ),
        (
            "Informacion Extra",
            {
                "fields": [
                    "investigacion_docentes",
                    "investigacion_estudiantes",
                    "extension_docentes",
                    "extension_estudiantes",
                ]
            },
        ),
    ]
