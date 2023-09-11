from django.contrib import admin


from .models import Usuario, Rol, Carrera, Asignatura, BloqueCurricular


@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


admin.site.register(Rol)
admin.site.register(Carrera)
admin.site.register(Asignatura)
admin.site.register(BloqueCurricular)
