from django.core.exceptions import ValidationError

from backend.common.funciones_fecha import obtener_fecha_actual
from backend.models import Configuracion
from backend.common.choices import ParametrosDeConfiguracion
from backend.services.semestre import ServicioSemestre
from backend.common.mensajes_de_error import (
    MENSAJE_NO_FUE_DEFINIDO_PERIODO_VALIDACION,
    MENSAJE_NO_FUE_DEFINIDO_PERIODO_CORRECCION,
    MENSAJE_NO_FUE_DEFINIDO_PERIODO_MODIFICACION,
)


class ServicioConfiguracion:
    servicio_semestre = ServicioSemestre()

    def obtener_dias_restantes_inicio_periodo_modificacion(self) -> int:
        """
        Retorna cuantos dias faltan para el proximo periodo de modificacion. Retorna 0 si ya comenzo el periodo de modificacion.
        """

        try:
            dias_antes_periodo_modificacion = Configuracion.objects.get(
                nombre=ParametrosDeConfiguracion.INICIO_PERIODO_MODIFICACION
            ).valor
        except Configuracion.DoesNotExist:
            raise ValidationError(
                {"__all__": MENSAJE_NO_FUE_DEFINIDO_PERIODO_MODIFICACION}
            )

        dias_restantes_inicio_semestre_siguiente = (
            self.obtener_dias_restantes_inicio_siguiente_semestre()
        )

        if dias_restantes_inicio_semestre_siguiente < dias_antes_periodo_modificacion:
            return 0
        else:
            return (
                dias_restantes_inicio_semestre_siguiente
                - dias_antes_periodo_modificacion
            )

    def obtener_dias_restantes_inicio_periodo_de_validacion(self) -> int:
        """
        Retorna cuantos dias faltan para el proximo periodo de validacion. Retorna 0 si ya comenzo el periodo de validacion.
        """

        try:
            dias_antes_periodo_validacion = Configuracion.objects.get(
                nombre=ParametrosDeConfiguracion.INICIO_PERIODO_VALIDACION
            ).valor
        except Configuracion.DoesNotExist:
            raise ValidationError(
                {"__all__": MENSAJE_NO_FUE_DEFINIDO_PERIODO_VALIDACION}
            )

        dias_restantes_inicio_semestre_siguiente = (
            self.obtener_dias_restantes_inicio_siguiente_semestre()
        )

        if dias_restantes_inicio_semestre_siguiente < dias_antes_periodo_validacion:
            return 0
        else:
            return (
                dias_restantes_inicio_semestre_siguiente - dias_antes_periodo_validacion
            )

    def obtener_dias_restantes_inicio_periodo_de_correccion(self) -> int:
        """
        Retorna cuantos dias faltan para el proximo periodo de correccion. Retorna 0 si ya comenzo el periodo de correccion.
        """

        try:
            dias_antes_periodo_correccion = Configuracion.objects.get(
                nombre=ParametrosDeConfiguracion.INICIO_PERIODO_CORRECCION
            ).valor
        except Configuracion.DoesNotExist:
            raise ValidationError(
                {"__all__": MENSAJE_NO_FUE_DEFINIDO_PERIODO_CORRECCION}
            )

        dias_restantes_inicio_semestre_siguiente = (
            self.obtener_dias_restantes_inicio_siguiente_semestre()
        )

        if dias_restantes_inicio_semestre_siguiente < dias_antes_periodo_correccion:
            return 0
        else:
            return (
                dias_restantes_inicio_semestre_siguiente - dias_antes_periodo_correccion
            )

    def obtener_dias_restantes_inicio_siguiente_semestre(self) -> int:
        hoy = obtener_fecha_actual()
        proximo_semestre = self.servicio_semestre.obtener_semestre_siguiente()
        dias_restantes = proximo_semestre.fecha_inicio - hoy

        return dias_restantes.days
