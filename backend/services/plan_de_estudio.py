from django.db.models import QuerySet, Q

from backend.common.funciones_fecha import obtener_fecha_actual
from backend.models import PlanDeEstudio


class ServicioPlanDeEstudio:
    def obtener_planes_activos_de_carrera(self) -> QuerySet[PlanDeEstudio]:
        hoy = obtener_fecha_actual()
        date_filter = Q(fecha_fin__isnull=True) | Q(
            fecha_fin__isnull=False, fecha_fin__gte=hoy
        )

        return PlanDeEstudio.objects.filter(date_filter, fecha_inicio__lte=hoy)
