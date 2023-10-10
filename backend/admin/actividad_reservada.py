from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest

from backend.models import ActividadReservada


class AdminActividadReservada(admin.ModelAdmin):
    model = ActividadReservada
    list_display = ["descripcion", "estandar"]
