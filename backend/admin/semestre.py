from django.contrib import admin
from django.http.request import HttpRequest

from backend.models import Rol
from backend.common.choices import Roles
from backend.forms import FormSemestre


class AdminSemestre(admin.ModelAdmin):
    form = FormSemestre

    def has_permission(self, request):
        user = request.user
        if user.is_superuser:
            return True

        roles = Rol.objects.filter(usuario=user)

        for rol in roles:
            if rol.rol == Roles.SECRETARIO:
                return True

        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return self.has_permission(request)

    def has_change_permission(self, request: HttpRequest, obj=...) -> bool:
        return self.has_permission(request)

    def has_add_permission(self, request: HttpRequest, obj=...) -> bool:
        return self.has_permission(request)
