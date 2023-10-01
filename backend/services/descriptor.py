from backend.models import Carrera, Descriptor


class ServicioDescriptor:
    def listar_actividades_reservadas(self, carrera: Carrera) -> list[Descriptor]:
        """Lista las actividades reservadas para una determinada carrera, dependiendo del estandar actual."""

        return []
