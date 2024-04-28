from backend.models import Estandar, Carrera


class ServicioEstandar:
    def obtener_estandar_activo_de_carrera(self, carrera=Carrera) -> Estandar:
        return (
            Estandar.objects.filter(carrera_id=carrera.id)
            .order_by("-fecha_inicio")
            .first()
        )
