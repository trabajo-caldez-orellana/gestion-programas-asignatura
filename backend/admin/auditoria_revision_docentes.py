from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest


class AdminAuditoriaRevisionDocentes(admin.ModelAdmin):
    list_display = ["version_programa", "accion", "modificado_en"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj=...) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj=...) -> bool:
        return False
