from django.db import models


class Carrera(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
