from django.contrib import admin


class AdminConfiguracion(admin.ModelAdmin):
    list_display = ["nombre", "valor"]
