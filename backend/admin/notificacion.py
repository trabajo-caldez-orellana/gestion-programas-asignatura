from django.contrib import admin


class AdminNotificacion(admin.ModelAdmin):
    list_display = ["usuario", "tipo", "fue_leida"]
    readonly_fields = ["creada", "leida"]
