from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest

from backend.models import Rol
from backend.common.choices import Roles


class AdminEstandar(admin.ModelAdmin):
    list_display = ["nombre", "fecha_inicio", "carrera"]
    filter_horizontal = ["descriptores"]

    def has_permission(self, request):
        user = request.user
        if user.is_superuser:
            return True

        roles = Rol.objects.filter(user=user)

        for rol in roles:
            if rol.rol == Roles.SECRETARIO:
                return True

        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return self.has_permission(request)

    def has_change_permission(self, request: HttpRequest, obj=...) -> bool:
        return self.has_permission(request)

    def has_delete_permission(self, request: HttpRequest, obj=...) -> bool:
        return self.has_permission(request)
