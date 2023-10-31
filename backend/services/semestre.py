from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import Semestre
from backend.common.mensajes_de_error import (
    MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
    MENSAJE_FECHAS_INCORRECTAS,
    MENSAJE_NO_HAY_SEMESTRE_ACTIVO,
    MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
    MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
)


class ServicioSemestre:
    def validar_semestre(
        self,
        fecha_inicio: timezone.datetime.date,
        fecha_fin: timezone.datetime.date,
        instance: Semestre | None = None,
    ):
        if fecha_inicio > fecha_fin:
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_FECHAS_INCORRECTAS,
                    "fecha_fin": MENSAJE_FECHAS_INCORRECTAS,
                }
            )

        if instance is not None:
            semestres_en_la_fecha = Semestre.objects.filter(
                fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio
            )
        else:
            semestres_en_la_fecha = Semestre.objects.filter(
                fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio
            ).exclude(id=instance.id)

        if semestres_en_la_fecha.exists():
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
                    "fecha_fin": MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
                }
            )

    def obtener_semestre_actual(self):
        hoy = timezone.now().astimezone()

        semestre = Semestre.objects.filter(
            fecha_inicio__lte=hoy, fecha_fin__gte=hoy
        ).first()

        if not semestre.exists():
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRE_ACTIVO})

        return semestre

    def obtener_semestre_anterior(self):
        # Semestres ordenados por fecha fin de menor a mayor
        semestres = Semestre.objects.all().order_by("fecha_inicio")

        indice_semestre_actual = None
        for indice in range(len(semestres)):
            if semestres[indice].esta_activo:
                indice_semestre_actual = indice

        if indice_semestre_actual == 0 or indice_semestre_actual is None:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_ANTERIORES})
        return semestres[indice_semestre_actual - 1]

    def obtener_semestre_siguiente(self) -> Semestre:
        # Semestres ordenados por fecha fin de mayor a menorr
        semestres = Semestre.objects.all().order_by("-fecha_inicio")

        indice_semestre_actual = None
        for indice in range(len(semestres)):
            if semestres[indice].esta_activo:
                indice_semestre_actual = indice

        if indice_semestre_actual == 0 or indice_semestre_actual is None:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_FUTUROS})
        return semestres[indice_semestre_actual - 1]
