from django.contrib import admin

from backend.models import (
    ProgramaTieneDescriptor,
    ProgramaTieneActividadReservada,
    Correlativa,
)


class DescriptorInline(admin.TabularInline):
    model = ProgramaTieneDescriptor


class ActividadReservadaInline(admin.TabularInline):
    model = ProgramaTieneActividadReservada


class CorrelativaInline(admin.TabularInline):
    model = Correlativa


class AdminVersionProgramaAsignatura(admin.ModelAdmin):
    list_display = ["asignatura", "semestre", "estado"]
    inlines = [
        DescriptorInline,
        ActividadReservadaInline,
        CorrelativaInline,
    ]

    fieldsets = [
        (
            None,
            {"fields": ["asignatura", "semestre", "estado"]},
        ),
        (
            "Informacion del Cursado",
            {
                "fields": [
                    "contenidos",
                    "bibliografia",
                    "recursos",
                    "evaluacion",
                    "cronograma",
                    "resultados_de_aprendizaje",
                    "fundamentacion",
                    "metodologia_aplicada",
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
