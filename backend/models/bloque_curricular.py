from django.db import models


class BloqueCurricular(models.Model):
    nombre = models.CharField(max_length=255)

    # NOTA. Cuantos digitos y cuantos lugares decimales?
    coeficiente = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Bloques Curriculares"
