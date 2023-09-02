from django.contrib import admin


from .models import Usuario


@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]
