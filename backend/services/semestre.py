from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import Semestre
from backend.common.mensajes_de_error import (
    MENSAJE_NO_HAY_SEMESTRE_ACTIVO,
    MENSAJE_NO_SE_CREARON_SEMESTRES,
    MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
)


class ServicioSemestre:
    def obtener_semestre_actual(self):
        hoy = timezone.now().astimezone()

        semestre = Semestre.objects.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy)

        if not semestre.exists():
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRE_ACTIVO})

        if len(semestre) > 1:
            semestre_actual = semestre.order_by("-fecha_fin").first()
        else:
            semestre_actual = semestre[0]

        return semestre_actual

    def obtener_semestre_anterior(self):
        hoy = timezone.now().astimezone()

        # Semestres ordenados por fecha fin de mayor a menor
        semestres = Semestre.objects.all().order_by("-fecha_fin")

        if not semestres.exists():
            raise ValidationError({"__all__": MENSAJE_NO_SE_CREARON_SEMESTRES})

        if not semestres.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy):
            # Si no hay un semestre activo retorna el primero de la lista
            return semestres.first()
        else:
            if len(semestres) == 1:
                raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_ANTERIORES})
            return semestres[1]
