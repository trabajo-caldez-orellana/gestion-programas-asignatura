from django.utils import timezone
from django.core.exceptions import ValidationError

from backend.models import Semestre, AnioAcademico
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual
from backend.common.choices import Semestres
from backend.common.mensajes_de_error import (
    MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
    MENSAJE_FECHAS_INCORRECTAS,
    MENSAJE_NO_HAY_SEMESTRE_ACTIVO,
    MENSAJE_NO_HAY_SEMESTRES_FUTUROS,
    MENSAJE_NO_HAY_SEMESTRES_ANTERIORES,
    MENSAJE_SEMESTRE_DEBE_PERTENECER_A_ANIO_LECTIVO,
    MENSAJE_TIPO_SEMESTRE_REPETIDO,
    MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
)


class ServicioSemestre:
    # TODO. buscar una manera de hacer esto mas eficiente y no hacer tantas Queries
    def validar_semestre(
        self,
        fecha_inicio: timezone.datetime.date,
        fecha_fin: timezone.datetime.date,
        anio_academico: AnioAcademico,
        tipo_semestre: Semestres,
        instance: Semestre | None = None,
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
        if instance is not None:
            semestres_en_la_fecha = semestres_en_la_fecha.exclude(id=instance.id)

        if bool(semestres_en_la_fecha):
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
                    "fecha_fin": MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA,
                }
            )

        if (
            fecha_inicio < anio_academico.fecha_inicio
            or fecha_fin > anio_academico.fecha_fin
        ):
            raise ValidationError(
                {
                    "fecha_inicio": MENSAJE_SEMESTRE_DEBE_PERTENECER_A_ANIO_LECTIVO,
                    "fecha_fin": MENSAJE_SEMESTRE_DEBE_PERTENECER_A_ANIO_LECTIVO,
                }
            )

        semestre_del_mismo_tipo_en_mismo_anio = Semestre.objects.filter(
            anio_academico_id=anio_academico.id, semestre=tipo_semestre
        )
        if instance is not None:
            semestre_del_mismo_tipo_en_mismo_anio = (
                semestre_del_mismo_tipo_en_mismo_anio.exclude(id=instance.id)
            )

        if bool(semestre_del_mismo_tipo_en_mismo_anio):
            raise ValidationError({"semestre": MENSAJE_TIPO_SEMESTRE_REPETIDO})

        # Fijarse si ya hay alguna instancia de un semestre para el año académico.
        # Y comparar que si son de distinto tipo, las fechas coincidan para que el
        # segundo semestre sea despues del primer semestre

        # Para este punto ya se que no se repite el mismo tipo de semestre, y que las fechas del semestre
        # que se esta creando/modificando.
        tipo = (
            Semestres.PRIMER
            if tipo_semestre == Semestres.SEGUNDO
            else Semestres.SEGUNDO
        )

        try:
            semestre_del_anio = Semestre.objects.get(
                anio_academico=anio_academico, semestre=tipo
            )

            if tipo_semestre == Semestres.PRIMER:
                if semestre_del_anio.fecha_fin < fecha_fin:
                    raise ValidationError(
                        {
                            "semestre": MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
                            "fecha_inicio": MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
                            "fecha_fin": MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
                        }
                    )
            else:
                if semestre_del_anio.fecha_fin > fecha_fin:
                    raise ValidationError(
                        {
                            "semestre": MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
                            "fecha_inicio": MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
                            "fecha_fin": MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO,
                        }
                    )
        except Semestre.DoesNotExist:
            pass

    def obtener_semestre_actual(self):
        hoy = obtener_fecha_y_hora_actual()

        semestre = Semestre.objects.filter(
            fecha_inicio__lte=hoy, fecha_fin__gte=hoy
        ).first()

        if not semestre:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRE_ACTIVO})

        return semestre

    def obtener_semestre_anterior(self, tipo_semestre: Semestres = None):
        # Semestres ordenados por fecha fin de menor a mayor
        semestres = Semestre.objects.all().order_by("fecha_inicio")

        indice_semestre_actual = None
        for indice in range(len(semestres)):
            if semestres[indice].esta_activo:
                indice_semestre_actual = indice

        if indice_semestre_actual == 0 or indice_semestre_actual is None:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_ANTERIORES})

        semestre_actual = semestres[indice_semestre_actual]
        if tipo_semestre is None or tipo_semestre != semestre_actual.semestre:
            return semestres[indice_semestre_actual - 1]
        else:
            if indice_semestre_actual == 1:
                raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_ANTERIORES})
            return semestres[indice_semestre_actual - 2]

    def obtener_semestre_siguiente(self, tipo_semestre: Semestres = None) -> Semestre:
        # Semestres ordenados por fecha fin de mayor a menorr
        semestres = Semestre.objects.all().order_by("-fecha_inicio")

        indice_semestre_actual = None
        for indice in range(len(semestres)):
            if semestres[indice].esta_activo:
                indice_semestre_actual = indice

        if indice_semestre_actual == 0 or indice_semestre_actual is None:
            raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_FUTUROS})

        semestre_actual = semestres[indice_semestre_actual]
        if tipo_semestre is None or tipo_semestre != semestre_actual.semestre:
            return semestres[indice_semestre_actual - 1]
        else:
            if indice_semestre_actual == 1:
                raise ValidationError({"__all__": MENSAJE_NO_HAY_SEMESTRES_FUTUROS})
            return semestres[indice_semestre_actual - 2]
