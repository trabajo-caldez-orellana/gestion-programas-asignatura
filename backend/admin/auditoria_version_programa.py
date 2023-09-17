from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest


class AdminAuditoriaEstadoVersionPrograma(admin.ModelAdmin):
    list_display = ["version_programa", "estado", "modificado_en"]
    readonly_fields = ["version_programa", "estado", "modificado_en", "rol"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=...) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=...) -> bool:
        return False
