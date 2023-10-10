from django.contrib import admin

from backend.models import Rol


class RolInline(admin.TabularInline):
    model = Rol


class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]
    inlines = [RolInline]
