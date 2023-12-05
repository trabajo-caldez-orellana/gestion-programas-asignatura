from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import Semestre, AnioAcademico
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual
from backend.common.mensajes_de_error import (
    MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
    MENSAJE_FECHAS_INCORRECTAS,
    MENSAJE_NO_HAY_ANIO_ACTIVO,
    MENSAJE_NO_HAY_ANIOS_ANTERIORES,
    MENSAJE_NO_HAY_ANIOS_FUTUROS,
)


class ServicioAnioAcademico:
    def validar_anio_academico(
        self,
        fecha_inicio: timezone.datetime.date,
        fecha_fin: timezone.datetime.date,
        instance: AnioAcademico | None = None,
    ):
        if fecha_inicio > fecha_fin:
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_FECHAS_INCORRECTAS,
                    "fecha_fin": MENSAJE_FECHAS_INCORRECTAS,
                }
            )

        anios_academicos_en_la_fecha = AnioAcademico.objects.filter(
            fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio
        )
        if instance is not None:
            anios_academicos_en_la_fecha = anios_academicos_en_la_fecha.exclude(
                id=instance.id
            )

        if anios_academicos_en_la_fecha.exists():
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
                    "fecha_fin": MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA,
                }
            )

    def obtener_anio_academico_actual(self) -> AnioAcademico:
        hoy = obtener_fecha_y_hora_actual()

        anio_academico = AnioAcademico.objects.filter(
            fecha_inicio__lte=hoy, fecha_fin__gte=hoy
        ).first()

        if not anio_academico:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_ANIO_ACTIVO})

        return anio_academico

    def obtener_anio_academico_anterior(self) -> AnioAcademico:
        # Anios academicos ordenados por fecha fin de menor a mayor
        anios_academicos = Semestre.objects.all().order_by("fecha_inicio")

        indice_anio_actual = None
        for indice in range(len(anios_academicos)):
            if anios_academicos[indice].esta_activo:
                indice_anio_actual = indice

        if indice_anio_actual == 0 or indice_anio_actual is None:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_ANIOS_ANTERIORES})
        return anios_academicos[indice_anio_actual - 1]

    def obtener_anio_academico_siguiente(self) -> AnioAcademico:
        # Anios academicos ordenados por fecha fin de mayor a menor
        anios_academicos = Semestre.objects.all().order_by("-fecha_inicio")

        indice_anio_actual = None
        for indice in range(len(anios_academicos)):
            if anios_academicos[indice].esta_activo:
                indice_anio_actual = indice

        if indice_anio_actual == 0 or indice_anio_actual is None:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_ANIOS_FUTUROS})
        return anios_academicos[indice_anio_actual - 1]
