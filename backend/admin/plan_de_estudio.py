from django.contrib import admin


class AdminPlanDeEstudio(admin.ModelAdmin):
    list_display = ["nombre", "esta_activo"]
    filter_horizontal = ["asignaturas"]
