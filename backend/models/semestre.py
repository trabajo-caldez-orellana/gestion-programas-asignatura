from django.db import models


class Semestre(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return "{} - {}".format(self.fecha_inicio, self.fecha_fin)
