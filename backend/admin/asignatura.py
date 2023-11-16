from django.contrib import admin


class AdminAsignatura(admin.ModelAdmin):
    list_display = ["codigo", "denominacion", "horas_semanales_clases", "carga_total"]
