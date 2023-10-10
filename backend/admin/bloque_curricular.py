from django.contrib import admin


class AdminBloqueCurricular(admin.ModelAdmin):
    list_display = ["nombre", "coeficiente"]
