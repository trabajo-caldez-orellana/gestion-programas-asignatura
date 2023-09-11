from django.db import models


class Configuracion(models.Model):
    nombre = models.CharField(unique=True, max_length=255)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Configuraciones"
