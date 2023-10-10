from django.contrib import admin


class AdminDescriptor(admin.ModelAdmin):
    list_display = ["descripcion", "tipo"]
