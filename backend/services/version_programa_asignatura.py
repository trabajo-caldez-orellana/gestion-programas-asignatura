from backend.models import (
    BloqueCurricular,
    VersionProgramaAsignatura,
    Asignatura,
    Descriptor,
    ActividadReservada,
)
from backend.common.choices import NivelDescriptor


class ServicioVersionProgramaAsignatura:
    def _asignar_carga_horaria(
        self, bloque: BloqueCurricular, programa: VersionProgramaAsignatura, carga: int
    ):
        """
        Asigna a una version de programa una carga horaria para un determinado bloque curricular.
        Verifica que la asignatura relacionada al programa tenga el mismo bloque curricular que el referenciado.

        Tira ValidationError cuando falla la validacion, con codigos de error: "bloque", "programa", "carga"
        """

        pass

    def reutilizar_ultimo_plan(self, asignatura: Asignatura):
        """
        Toma la ultima version del plan de la asignatura, y crea una nueva con los mismos datos y presenta para aprobacion.
        """

        pass

    def _asignar_descriptor(
        self,
        descriptor: Descriptor,
        programa: VersionProgramaAsignatura,
        nivel: NivelDescriptor,
    ):
        """
        Agrega un descriptor a un cierto programa de asignatura. Verifica que el descriptor seleccionado
        pertenezca al estandar de alguna de las carreras que tienen la asignatura.
        Ademas, verifica el tipo de descriptor segun el nivel.
        """

        pass

    def _asignar_actividad_reservada(
        self,
        actividad: ActividadReservada,
        programa: VersionProgramaAsignatura,
        nivel: NivelDescriptor,
    ):
        """
        Agrega una actividad reservada a un cierto programa de asignatura. Verifica que la actividad seleccionada
        pertenezca al estandar de alguna de las carreras que tienen la asignatura.
        """

        pass
