from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import Semestre
from backend.common.mensajes_de_error import (
    MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
    MENSAJE_FECHAS_INCORRECTAS,
)


class ServicioSemestre:
    def validar_semestre(
        self, fecha_inicio: timezone.datetime.date, fecha_fin: timezone.datetime.date
    ):
        if fecha_inicio > fecha_fin:
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_FECHAS_INCORRECTAS,
                    "fecha_fin": MENSAJE_FECHAS_INCORRECTAS,
                }
            )

        semestres_en_la_fecha = Semestre.objects.filter(
            fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio
        )

        if semestres_en_la_fecha.exists():
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
                    "fecha_fin": MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
                }
            )
