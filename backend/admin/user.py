from typing import Any, Dict, List, Tuple

from django.contrib.auth import admin
from django.contrib.admin import TabularInline
from django.http.request import HttpRequest
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AdminPasswordChangeForm,
)

from backend.models import Rol, Usuario

USER_PERSONAL_INFO_FIELDS = ("first_name", "last_name", "profile_picture")
USER_CREATION_FIELDS = ("email", "password1", "password2")


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = USER_PERSONAL_INFO_FIELDS + USER_CREATION_FIELDS


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = USER_PERSONAL_INFO_FIELDS + ("email",)


class ChangePasswordForm(AdminPasswordChangeForm):
    def clean(self) -> dict[str, Any]:
        return super().clean()


class RolInline(TabularInline):
    model = Rol


class UserAdmin(admin.UserAdmin):
    model = Usuario
    add_form = CreateUserForm
    form = ChangeUserForm
    change_password_form = ChangePasswordForm

    list_display = ["first_name", "last_name", "email"]
    ordering = ["email"]
    inlines = [RolInline]

    def get_fieldsets(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> List[Tuple[str | None, Dict[str, Any]]]:
        if not obj:
            fieldsets = [
                (
                    None,
                    {
                        "classes": ("wide",),
                        "fields": ("email", "password1", "password2"),
                    },
                ),
                ("Personal info", {"fields": USER_PERSONAL_INFO_FIELDS}),
            ]

        else:  # This is for editing an existing user
            fieldsets = (
                (None, {"fields": ("email", "password")}),
                ("Personal info", {"fields": USER_PERSONAL_INFO_FIELDS}),
            )

        fieldsets += (
            (
                "Permissions",
                {
                    "fields": (
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    ),
                },
            ),
        )

        return fieldsets
