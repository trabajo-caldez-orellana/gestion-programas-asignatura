from django.db import models

from backend.common.choices import ParametrosDeConfiguracion


class Configuracion(models.Model):
    nombre = models.CharField(
        unique=True, max_length=255, choices=ParametrosDeConfiguracion.choices
    )
    valor = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Configuraciones"
