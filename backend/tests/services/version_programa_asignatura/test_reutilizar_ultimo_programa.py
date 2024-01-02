import json
from freezegun import freeze_time

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.services import ServicioVersionProgramaAsignatura
from backend.tests.utils import (
    set_up_tests,
    CODIGO_ASIGNATURA_1,
    CODIGO_ASIGNATURA_2,
    CARRERA_1,
    CARRERA_2,
    DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA_PARA_REUTILIZAR,
    DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE,
    crear_configuraciones_del_prograna,
    crear_anios_de_prueba,
    crear_fecha_y_hora,
    FECHA_DEFAULT_MODIFICACION,
    FECHA_INICIO_ANIO_ABIERTO,
    FECHA_FIN_ANIO_ABIERTO,
    FECHA_FIN_ANIO_CERRADO,
    FECHA_FIN_ANIO_FUTURO,
    FECHA_INICIO_ANIO_CERRADO,
    FECHA_INICIO_ANIO_FUTURO,
)
from backend.models import (
    Asignatura,
    VersionProgramaAsignatura,
    Configuracion,
    ProgramaTieneActividadReservada,
    ProgramaTieneDescriptor,
    Carrera,
    Estandar,
    ActividadReservada,
    Semestre,
)
from backend.common.mensajes_de_error import (
    MENSAJE_DESCRIPTOR,
    MENSAJE_EJE_TRANSVERAL,
    MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES,
    MENSAJE_VERSION_ANTERIOR_NO_APROBADA,
    MENSAJE_CANTIDAD_DE_RESULTADOS,
    MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR,
    MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
    MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
    MENSAJE_PROGRAMAS_CERRADOS,
)
from backend.common.choices import (
    EstadoAsignatura,
    NivelDescriptor,
    TipoDescriptor,
    ParametrosDeConfiguracion,
    Semestres,
)
from backend.common.constantes import (
    MINIMO_RESULTADOS_DE_APRENDIZAJE,
    MAXIMO_RESULTADOS_DE_APRENDIZAJE,
)


class TestReutilizarUltimoPrograna(TestCase):
    servicio_version_programa_asignatura = ServicioVersionProgramaAsignatura()

    def setUp(self):
        (
            self.anio_cerrado,
            self.anio_actual,
            self.anio_futuro,
        ) = crear_anios_de_prueba()

        # Creo dos semestres por anio. Anio Cerrado:
        dias_anio = FECHA_FIN_ANIO_CERRADO - FECHA_INICIO_ANIO_CERRADO
        self.primer_semestre_anio_cerrado = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_CERRADO,
            fecha_fin=(
                FECHA_INICIO_ANIO_CERRADO + timezone.timedelta(dias_anio.days / 2)
            ),
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_cerrado,
        )
        self.segundo_semestre_anio_cerrado = Semestre.objects.create(
            fecha_inicio=(
                FECHA_INICIO_ANIO_CERRADO + timezone.timedelta(dias_anio.days / 2 + 1)
            ),
            fecha_fin=FECHA_FIN_ANIO_CERRADO,
            semestre=Semestres.SEGUNDO,
            anio_academico=self.anio_cerrado,
        )

        # Creo dos semestres por anio. Anio abierto:
        dias_anio = FECHA_FIN_ANIO_ABIERTO - FECHA_INICIO_ANIO_ABIERTO
        self.primer_semestre_anio_abierto = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_ABIERTO,
            fecha_fin=(
                FECHA_INICIO_ANIO_ABIERTO + timezone.timedelta(dias_anio.days / 2)
            ),
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_actual,
        )
        self.segundo_semestre_anio_abierto = Semestre.objects.create(
            fecha_inicio=(
                FECHA_INICIO_ANIO_ABIERTO + timezone.timedelta(dias_anio.days / 2 + 1)
            ),
            fecha_fin=FECHA_FIN_ANIO_ABIERTO,
            semestre=Semestres.SEGUNDO,
            anio_academico=self.anio_actual,
        )

        # Creo dos semestres por anio. Anio futuro:
        dias_anio = FECHA_FIN_ANIO_FUTURO - FECHA_INICIO_ANIO_FUTURO
        self.primer_semestre_anio_futuro = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_FUTURO,
            fecha_fin=FECHA_INICIO_ANIO_FUTURO + timezone.timedelta(dias_anio.days / 2),
            semestre=Semestres.PRIMER,
            anio_academico=self.anio_futuro,
        )
        self.segundo_semestre_anio_futuro = Semestre.objects.create(
            fecha_inicio=FECHA_INICIO_ANIO_FUTURO
            + timezone.timedelta(dias_anio.days / 2 + 1),
            fecha_fin=FECHA_FIN_ANIO_FUTURO,
            semestre=Semestres.SEGUNDO,
            anio_academico=self.anio_futuro,
        )
        crear_configuraciones_del_prograna()
        set_up_tests()

        self.asignatura = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_1)
        self.asignatura_2 = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_2)
        self.carrera = Carrera.objects.get(nombre=CARRERA_1)
        self.carrera_2 = Carrera.objects.get(nombre=CARRERA_2)

    def _crear_version_anterior_con_datos_default(
        self, semestre: Semestre = None, asignatura: Asignatura = None
    ):
        if semestre is None:
            semestre_para_version = self.primer_semestre_anio_abierto
        else:
            semestre_para_version = semestre

        if asignatura is None:
            asignatura_para_version = self.asignatura
        else:
            asignatura_para_version = asignatura

        datos_version_anterior = {
            **DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA_PARA_REUTILIZAR
        }

        datos_version_anterior["semestre"] = semestre_para_version
        datos_version_anterior["asignatura"] = asignatura_para_version
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        return version_anterior

    def _agregar_descritpores_ejes_y_actividaddes(
        self, version_programa: VersionProgramaAsignatura
    ):
        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        # Agrego actividades reservadas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )

        ProgramaTieneActividadReservada.objects.create(
            version_programa_asignatura=version_programa,
            actividad_reservada=actividades_reservadas_carrera.first(),
            nivel=NivelDescriptor.BAJO,
        )

        descriptores_carrera = estandar_carrera.descriptores.all()
        # Agrego ejes transversales
        ejes_transversales = descriptores_carrera.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )
        for eje in ejes_transversales:
            ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_programa,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego descriptores
        descriptores = descriptores_carrera.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_programa,
                nivel=NivelDescriptor.BAJO,
            )

    def test_no_hay_version_anterior_disponible(self):
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )

            self.assertIn("asignatura", context.exception.message_dict)
            self.assertIn(
                MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES,
                context.exception.message_dict.get("asignatura"),
            )

    def test_version_anterior_no_aprobada(self):
        datos_version_anterior = {
            **DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA_PARA_REUTILIZAR
        }
        datos_version_anterior["asignatura"] = self.asignatura
        datos_version_anterior["estado"] = EstadoAsignatura.PENDIENTE

        datos_version_anterior["semestre"] = self.primer_semestre_anio_abierto
        VersionProgramaAsignatura.objects.create(**datos_version_anterior)

        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        asignatura=self.asignatura
                    )
                )
            self.assertIn("asignatura", context.exception.message_dict)
            self.assertIn(
                MENSAJE_VERSION_ANTERIOR_NO_APROBADA,
                context.exception.message_dict.get("asignatura"),
            )

    def test_no_es_periodo_de_actualizacion_de_programas(self):
        # Cambio las configuraciones para hacer mas corto el periodo de actualizacion.
        configuracion_modificacion = Configuracion.objects.get(
            nombre=ParametrosDeConfiguracion.INICIO_PERIODO_MODIFICACION
        )
        configuracion_modificacion.valor = 3
        configuracion_modificacion.full_clean()
        configuracion_modificacion.save()

        configuracion_validacion = Configuracion.objects.get(
            nombre=ParametrosDeConfiguracion.INICIO_PERIODO_VALIDACION
        )
        configuracion_validacion.valor = 2
        configuracion_validacion.full_clean()
        configuracion_validacion.save()

        configuracion_correccion = Configuracion.objects.get(
            nombre=ParametrosDeConfiguracion.INICIO_PERIODO_CORRECCION
        )
        configuracion_correccion.valor = 1
        configuracion_correccion.full_clean()
        configuracion_correccion.save()

        version_anterior = self._crear_version_anterior_con_datos_default()
        self._agregar_descritpores_ejes_y_actividaddes(
            version_programa=version_anterior
        )
        with self.assertRaises(ValidationError) as excepcion:
            self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                self.asignatura
            )

        self.assertIn("__all__", excepcion.exception.message_dict)
        self.assertIn(
            MENSAJE_PROGRAMAS_CERRADOS, excepcion.exception.message_dict["__all__"]
        )

    def test_programa_anterior_no_es_valido_descriptor_de_otra_carrera(self):
        version_anterior = self._crear_version_anterior_con_datos_default()
        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        # Agrego Actividades reservadas correctas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )
        programa_tiene_actividad_reservada = (
            ProgramaTieneActividadReservada.objects.create(
                version_programa_asignatura=version_anterior,
                actividad_reservada=actividades_reservadas_carrera.first(),
                nivel=NivelDescriptor.BAJO,
            )
        )

        descriptores_estandar = estandar_carrera.descriptores.all()
        # Agrego ejes correctos
        ejes_transversales = descriptores_estandar.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )
        for eje in ejes_transversales:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego descriptores de otra carrera
        estandar_carrera_2 = Estandar.objects.get(carrera=self.carrera_2)
        descriptores_estandar_2 = estandar_carrera_2.descriptores.all()
        descriptores = descriptores_estandar_2.filter(tipo=TipoDescriptor.DESCRIPTOR)

        for descriptor in descriptores:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento poder crear uno nuevo, deberia fallar:
        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        asignatura=self.asignatura
                    )
                )

            self.assertIn("descriptores", context.exception.message_dict)
            self.assertIn(
                MENSAJE_DESCRIPTOR, context.exception.message_dict.get("descriptores")
            )

    def test_programa_anterior_no_es_valido_eje_de_otra_carrera(self):
        version_anterior = self._crear_version_anterior_con_datos_default()
        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        # Agrego Actividades reservadas correctas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )

        programa_tiene_actividad_reservada = (
            ProgramaTieneActividadReservada.objects.create(
                version_programa_asignatura=version_anterior,
                actividad_reservada=actividades_reservadas_carrera.first(),
                nivel=NivelDescriptor.BAJO,
            )
        )

        descriptores_estandar = estandar_carrera.descriptores.all()

        # Agrego descriptores correctos
        descriptores = descriptores_estandar.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego ejes transversales de otra carrera
        estandar_carrera_2 = Estandar.objects.get(carrera=self.carrera_2)
        ejes_transversales_estandar_2 = estandar_carrera_2.descriptores.all()
        descriptores = ejes_transversales_estandar_2.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )

        for descriptor in descriptores:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento poder crear uno nuevo, deberia fallar:
        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        asignatura=self.asignatura
                    )
                )

            self.assertIn("ejes_transversales", context.exception.message_dict)
            self.assertIn(
                MENSAJE_EJE_TRANSVERAL,
                context.exception.message_dict.get("ejes_transversales"),
            )

    def test_programa_anterior_no_es_valido_cantidad_de_resultados_menor_al_minimo(
        self,
    ):
        # Primero hago menos resultados que el minimo
        datos_version_anterior = {
            **DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA_PARA_REUTILIZAR
        }
        cantidad_resultados = MINIMO_RESULTADOS_DE_APRENDIZAJE - 1
        datos_version_anterior["resultados_de_aprendizaje"] = json.dumps(
            DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[:cantidad_resultados]
        )

        datos_version_anterior["semestre"] = self.primer_semestre_anio_abierto
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        # Agrego Actividades reservadas correctas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )

        programa_tiene_actividad_reservada = (
            ProgramaTieneActividadReservada.objects.create(
                version_programa_asignatura=version_anterior,
                actividad_reservada=actividades_reservadas_carrera.first(),
                nivel=NivelDescriptor.BAJO,
            )
        )

        descriptores_estandar = estandar_carrera.descriptores.all()

        # Agrego descriptores correctos
        descriptores = descriptores_estandar.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego ejes transversales de otra carrera
        ejes_transversales = descriptores_estandar.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )

        for eje in ejes_transversales:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento poder crear uno nuevo, deberia fallar:
        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        asignatura=self.asignatura
                    )
                )

            self.assertIn("resultados_de_aprendizaje", context.exception.message_dict)
            self.assertIn(
                MENSAJE_CANTIDAD_DE_RESULTADOS,
                context.exception.message_dict.get("resultados_de_aprendizaje"),
            )

    def test_programa_anterior_no_es_valido_cantidad_de_resultados_mayor_al_maximo(
        self,
    ):
        # Primero hago menos resultados que el minimo
        datos_version_anterior = {
            **DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA_PARA_REUTILIZAR
        }
        cantidad_resultados = MAXIMO_RESULTADOS_DE_APRENDIZAJE + 1
        datos_version_anterior["resultados_de_aprendizaje"] = json.dumps(
            DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[:cantidad_resultados]
        )

        datos_version_anterior["semestre"] = self.primer_semestre_anio_abierto
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        # Agrego Actividades reservadas correctas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )

        programa_tiene_actividad_reservada = (
            ProgramaTieneActividadReservada.objects.create(
                version_programa_asignatura=version_anterior,
                actividad_reservada=actividades_reservadas_carrera.first(),
                nivel=NivelDescriptor.BAJO,
            )
        )

        descriptores_estandar = estandar_carrera.descriptores.all()

        # Agrego descriptores correctos
        descriptores = descriptores_estandar.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego ejes transversales de otra carrera
        ejes_transversales = descriptores_estandar.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )

        for eje in ejes_transversales:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento poder crear uno nuevo, deberia fallar:
        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        asignatura=self.asignatura
                    )
                )

            self.assertIn("resultados_de_aprendizaje", context.exception.message_dict)
            self.assertIn(
                MENSAJE_CANTIDAD_DE_RESULTADOS,
                context.exception.message_dict.get("resultados_de_aprendizaje"),
            )

    def test_programa_anterior_no_tiene_descriptores(self):
        version_anterior = self._crear_version_anterior_con_datos_default()

        estandar_carrera = Estandar.objects.get(carrera=self.carrera)
        # Agrego actividades reservadas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )

        ProgramaTieneActividadReservada.objects.create(
            version_programa_asignatura=version_anterior,
            actividad_reservada=actividades_reservadas_carrera.first(),
            nivel=NivelDescriptor.BAJO,
        )

        descriptores_carrera = estandar_carrera.descriptores.all()
        # Agrego ejes transversales
        ejes_transversales = descriptores_carrera.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )
        for eje in ejes_transversales:
            ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        self.asignatura
                    )
                )

                self.assertIn("descriptor", context.exception.message_dict)
                self.assertIn(
                    MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR,
                    context.exception.message_dict.get("descriptor"),
                )

    def test_programa_anterior_no_tiene_ejes_transversales(self):
        version_anterior = self._crear_version_anterior_con_datos_default()

        estandar_carrera = Estandar.objects.get(carrera=self.carrera)
        # Agrego actividades reservadas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )

        ProgramaTieneActividadReservada.objects.create(
            version_programa_asignatura=version_anterior,
            actividad_reservada=actividades_reservadas_carrera.first(),
            nivel=NivelDescriptor.BAJO,
        )

        descriptores_carrera = estandar_carrera.descriptores.all()

        # Agrego descriptores
        descriptores = descriptores_carrera.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        self.asignatura
                    )
                )

                self.assertIn("eje_transversal", context.exception.message_dict)
                self.assertIn(
                    MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
                    context.exception.message_dict.get("eje_transversal"),
                )

    def test_programa_anterior_no_tiene_actividades_reservadas(self):
        version_anterior = self._crear_version_anterior_con_datos_default()

        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        descriptores_carrera = estandar_carrera.descriptores.all()
        # Agrego ejes transversales
        ejes_transversales = descriptores_carrera.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )
        for eje in ejes_transversales:
            ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego descriptores
        descriptores = descriptores_carrera.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            with self.assertRaises(ValidationError) as context:
                version_nueva = (
                    self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                        self.asignatura
                    )
                )

                self.assertIn("actividades_reservadas", context.exception.message_dict)
                self.assertIn(
                    MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
                    context.exception.message_dict.get("actividades_reservadas"),
                )

    def test_reutiliza_programa_correctamente(self):
        version_anterior = self._crear_version_anterior_con_datos_default()
        estandar_carrera = Estandar.objects.get(carrera=self.carrera)

        # Agrego Actividades reservadas correctas
        actividades_reservadas_carrera = ActividadReservada.objects.filter(
            estandar=estandar_carrera
        )
        programa_tiene_actividad_reservada = (
            ProgramaTieneActividadReservada.objects.create(
                version_programa_asignatura=version_anterior,
                actividad_reservada=actividades_reservadas_carrera.first(),
                nivel=NivelDescriptor.BAJO,
            )
        )

        descriptores_estandar = estandar_carrera.descriptores.all()
        # Agrego ejes correctos
        ejes_transversales = descriptores_estandar.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )
        for eje in ejes_transversales:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego descriptores de otra carrera
        descriptores = descriptores_estandar.filter(tipo=TipoDescriptor.DESCRIPTOR)

        for descriptor in descriptores:
            programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Ahora intento poder crear uno nuevo, deberia fallar:
        # Ahora intento reutilizar la version anterior
        fecha_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=FECHA_DEFAULT_MODIFICACION - 1)
        )

        with freeze_time(fecha_referencia):
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )

    def test_no_es_periodo_de_actualizacion_de_programas_programa_primer_semestre(self):
        self.asignatura.semestre_dictado = Semestres.PRIMER
        self.asignatura.full_clean()
        self.asignatura.save()

        # Sera período de actualización del segundo semestre, pero la materia es del primer semestre
        self._crear_version_anterior_con_datos_default(
            self.primer_semestre_anio_cerrado, self.asignatura
        )
        fecha_de_referencia = (
            self.segundo_semestre_anio_abierto.fecha_inicio
            - timezone.timedelta(days=10)
        )
        fecha_de_referencia = crear_fecha_y_hora(
            fecha_de_referencia.year, fecha_de_referencia.month, fecha_de_referencia.day
        )

        with freeze_time(fecha_de_referencia):
            with self.assertRaises(ValidationError) as context:
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )

        self.assertIn(
            MENSAJE_PROGRAMAS_CERRADOS, context.exception.message_dict["__all__"]
        )

    def test_no_es_periodo_de_actualizacion_de_programas_programa_segundo_semestre(
        self,
    ):
        self.asignatura.semestre_dictado = Semestres.SEGUNDO
        self.asignatura.full_clean()
        self.asignatura.save()

        # Sera período de actualización del primer semestre, pero la materia es del segundo semestre
        self._crear_version_anterior_con_datos_default(
            self.segundo_semestre_anio_cerrado, self.asignatura
        )
        fecha_de_referencia = (
            self.primer_semestre_anio_futuro.fecha_inicio - timezone.timedelta(days=10)
        )
        fecha_de_referencia = crear_fecha_y_hora(
            fecha_de_referencia.year, fecha_de_referencia.month, fecha_de_referencia.day
        )

        with freeze_time(fecha_de_referencia):
            with self.assertRaises(ValidationError) as context:
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )

        self.assertIn(
            MENSAJE_PROGRAMAS_CERRADOS, context.exception.message_dict["__all__"]
        )

    def test_reutiliza_programa_correctamente_materia_primer_semestre(self):
        self.asignatura.semestre_dictado = Semestres.PRIMER
        self.asignatura.full_clean()
        self.asignatura.save()

        version_anterior = self._crear_version_anterior_con_datos_default(
            self.primer_semestre_anio_cerrado, self.asignatura
        )
        self._agregar_descritpores_ejes_y_actividaddes(version_anterior)

        fecha_de_referencia = (
            self.primer_semestre_anio_futuro.fecha_inicio - timezone.timedelta(days=10)
        )
        fecha_de_referencia = crear_fecha_y_hora(
            fecha_de_referencia.year, fecha_de_referencia.month, fecha_de_referencia.day
        )

        with freeze_time(fecha_de_referencia):
            programa = self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                self.asignatura
            )
        self.assertEqual(programa.semestre, self.primer_semestre_anio_futuro)

    def test_reutiliza_programa_correctamente_materia_segundo_semestre(self):
        # Primero estando en el primer semestre
        self.asignatura.semestre_dictado = Semestres.SEGUNDO
        self.asignatura.full_clean()
        self.asignatura.save()

        version_anterior = self._crear_version_anterior_con_datos_default(
            self.segundo_semestre_anio_cerrado, self.asignatura
        )
        self._agregar_descritpores_ejes_y_actividaddes(version_anterior)

        fecha_de_referencia = (
            self.segundo_semestre_anio_futuro.fecha_inicio - timezone.timedelta(days=10)
        )
        fecha_de_referencia = crear_fecha_y_hora(
            fecha_de_referencia.year, fecha_de_referencia.month, fecha_de_referencia.day
        )

        with freeze_time(fecha_de_referencia):
            programa = self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                self.asignatura
            )
        self.assertEqual(programa.semestre, self.segundo_semestre_anio_futuro)
