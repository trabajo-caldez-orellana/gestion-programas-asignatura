from django.db import models
from django.core.exceptions import ValidationError

from backend.models.usuario import Usuario
from backend.models.carrera import Carrera
from backend.models.asignatura import Asignatura

from backend.common.choices import Roles, Dedicaciones
from backend.common.mensajes_de_error import (
    MENSAJE_DOCENTE_SELECCIONA_ASIGNATURA,
    MENSAJE_DIRECTOR_SELECCIONA_ASIGNATURA,
    MENSAJE_DIRECTOR_SELECCIONA_CARRERA,
    MENSAJE_DOCENTE_SELECCIONA_CARRERA,
    MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA,
)


class ManagerRol(models.Manager):
    def create(self, **kwargs):
        rol = self.model(**kwargs)
        rol.full_clean()
        rol.save()
        return rol


class Rol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carrera = models.ForeignKey(
        Carrera, on_delete=models.SET_NULL, null=True, blank=True
    )
    asignatura = models.ForeignKey(
        Asignatura, on_delete=models.SET_NULL, null=True, blank=True
    )
    rol = models.CharField(max_length=2, choices=Roles.choices)
    dedicacion = models.CharField(max_length=2, choices=Dedicaciones.choices)

    def get_dedicacion(self):
        return self.get_dedicacion_display()

    def get_rol(self):
        return self.get_rol_display()

    def __str__(self):
        return "{} - {}".format(self.rol, self.usuario)

    objects = ManagerRol()

    class Meta:
        verbose_name_plural = "Roles"

    def clean(self) -> None:
        error_message = {}

        if self.rol == Roles.DIRECTOR_CARRERA:
            if self.asignatura is not None:
                error_message["asignatura"] = MENSAJE_DIRECTOR_SELECCIONA_ASIGNATURA
            if self.carrera is None:
                error_message["carrera"] = MENSAJE_DIRECTOR_SELECCIONA_CARRERA

        if self.rol == Roles.DOCENTE or self.rol == Roles.TITULAR_CATEDRA:
            if self.asignatura is None:
                error_message["asignatura"] = MENSAJE_DOCENTE_SELECCIONA_ASIGNATURA
            if self.carrera is not None:
                error_message["carrera"] = MENSAJE_DOCENTE_SELECCIONA_CARRERA

        if self.rol == Roles.SECRETARIO:
            if self.asignatura is not None:
                error_message["asignatura"] = (
                    MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA
                )
            if self.carrera is not None:
                error_message["carrera"] = (
                    MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA
                )

        if error_message.keys:  # pragma: no branch
            raise ValidationError(error_message)
