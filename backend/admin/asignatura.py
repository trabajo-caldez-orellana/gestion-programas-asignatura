from django.contrib import admin


class AdminAsignatura(admin.ModelAdmin):
    list_display = ["codigo", "denominacion"]
