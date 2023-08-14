from django.db import models


class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
