import json
from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.services import ServicioVersionProgramaAsignatura
from backend.tests.utils import (
    set_up_tests,
    CODIGO_ASIGNATURA_1,
    CODIGO_ASIGNATURA_2,
    CARRERA_1,
    CARRERA_2,
    DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA,
    DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE,
    MENSAJE_SERVICIO_DEBE_FALLAR,
    crear_configuraciones_del_prograna,
    crear_semestres_de_prueba,
)
from backend.models import (
    Asignatura,
    VersionProgramaAsignatura,
    Configuracion,
    ProgramaTieneActividadReservada,
    ProgramaTieneDescriptor,
    CargaBloque,
    Carrera,
    Estandar,
    ActividadReservada,
)
from backend.common.mensajes_de_error import (
    MENSAJE_BLOQUE_CURRICUALR,
    MENSAJE_DESCRIPTOR,
    MENSAJE_EJE_TRANSVERAL,
    MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES,
    MENSAJE_VERSION_ANTERIOR_NO_APROBADA,
    MENSAJE_CANTIDAD_DE_RESULTADOS,
    MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
    MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
    MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR,
    MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
    MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
    MENSAJE_PROGRAMA_DEBE_TENER_CARGA_HORARIA,
)
from backend.common.choices import (
    EstadoAsignatura,
    NivelDescriptor,
    TipoDescriptor,
    ParametrosDeConfiguracion,
)
from backend.common.constantes import (
    MINIMO_RESULTADOS_DE_APRENDIZAJE,
    MAXIMO_RESULTADOS_DE_APRENDIZAJE,
)


# TODO. Completar tests cuando esto este terminado
class TestReutilizarUltimoPlan(TestCase):
    servicio_version_programa_asignatura = ServicioVersionProgramaAsignatura()

    def setUp(self):
        set_up_tests()
        crear_configuraciones_del_prograna()
        (
            self.semestre_anterior,
            self.semestre_actual,
            self.semestre_siguiente,
        ) = crear_semestres_de_prueba()

        self.asignatura = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_1)
        self.asignatura_2 = Asignatura.objects.get(codigo=CODIGO_ASIGNATURA_2)
        self.carrera = Carrera.objects.get(nombre=CARRERA_1)
        self.carrera_2 = Carrera.objects.get(nombre=CARRERA_2)

    def __crear_version_anterior_con_datos_default(self):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        return version_anterior

    def __agregar_descritpores_ejes_carga_y_actividaddes(
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

        # Agrego carga horaria al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_programa,
            bloque_curricular=self.asignatura.bloque_curricular,
        )

    def test_no_hay_version_anterior_disponible(self):
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )

            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)
        except ValidationError as e:
            self.assertIn("asignatura", e.message_dict)
            self.assertIn(
                MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES, e.message_dict.get("asignatura")
            )

    def test_version_anterior_no_aprobada(self):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior["asignatura"] = self.asignatura
        datos_version_anterior["estado"] = EstadoAsignatura.PENDIENTE

        datos_version_anterior["semestre"] = self.semestre_anterior
        version_anterior_sin_aprobar = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        # Ahora intento reutilizar la version anterior
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)
        except ValidationError as e:
            self.assertIn("asignatura", e.message_dict)
            self.assertIn(
                MENSAJE_VERSION_ANTERIOR_NO_APROBADA, e.message_dict.get("asignatura")
            )

    def test_no_es_periodo_de_actualizacion_de_programas(sef):
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

    def test_programa_anterior_no_es_valido_descriptor_de_otra_carrera(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()
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

        # Agrego carga horaria correcta al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
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
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("descriptor", e.message_dict)
            self.assertIn(MENSAJE_DESCRIPTOR, e.message_dict.get("descriptor"))

    def test_programa_anterior_no_es_valido_eje_de_otra_carrera(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()
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

        # Agrego carga horaria correcta al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
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
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("eje_transversal", e.message_dict)
            self.assertIn(MENSAJE_EJE_TRANSVERAL, e.message_dict.get("eje_transversal"))

    def test_programa_anterior_no_es_valido_carga_distinto_bloque(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()
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

        # Agrego descriptores correctos
        descriptores_carrera = estandar_carrera.descriptores.all()
        descriptores = descriptores_carrera.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego ejes transversales correctos
        ejes_transversales_carrera = estandar_carrera.descriptores.all()
        ejes_transverales = ejes_transversales_carrera.filter(
            tipo=TipoDescriptor.EJE_TRANSVERSAL
        )
        for eje in ejes_transverales:
            ProgramaTieneDescriptor.objects.create(
                descriptor=eje,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        # Agrego carga horaria de otro bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura_2.bloque_curricular,
        )

        # Ahora intento poder crear uno nuevo, deberia fallar:
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("bloque_curricular", e.message_dict)
            self.assertIn(
                MENSAJE_BLOQUE_CURRICUALR, e.message_dict.get("bloque_curricular")
            )

    def test_programa_anterior_no_es_valido_cantidad_de_resultados_menor_al_minimo(
        self,
    ):
        # Primero hago menos resultados que el minimo
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        cantidad_resultados = MINIMO_RESULTADOS_DE_APRENDIZAJE - 1
        datos_version_anterior["resultados_de_aprendizaje"] = json.dumps(
            DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[:cantidad_resultados]
        )

        datos_version_anterior["semestre"] = self.semestre_anterior
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

        # Agrego carga horaria correcta al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
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
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)
        except ValidationError as e:
            self.assertIn("resultados_de_aprendizaje", e.message_dict)
            self.assertIn(
                MENSAJE_CANTIDAD_DE_RESULTADOS,
                e.message_dict.get("resultados_de_aprendizaje"),
            )

    def test_programa_anterior_no_es_valido_cantidad_de_resultados_mayor_al_maximo(
        self,
    ):
        # Primero hago menos resultados que el minimo
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        cantidad_resultados = MAXIMO_RESULTADOS_DE_APRENDIZAJE + 1
        datos_version_anterior["resultados_de_aprendizaje"] = json.dumps(
            DATOS_DEFAULT_RESULTADOS_DE_APRENDIZAJE[:cantidad_resultados]
        )

        datos_version_anterior["semestre"] = self.semestre_anterior
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

        # Agrego carga horaria correcta al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
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
        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    asignatura=self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("resultados_de_aprendizaje", e.message_dict)
            self.assertIn(
                MENSAJE_CANTIDAD_DE_RESULTADOS,
                e.message_dict.get("resultados_de_aprendizaje"),
            )

    def test_programa_anterior_no_es_valido_horario_teoria_faltante_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior.pop("semanal_teoria_presencial")

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_teoria_presencial", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_teoria_presencial"),
            )

    def test_programa_anterior_no_es_valido_horario_practica_faltante_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior.pop("semanal_practica_presencial")

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_practica_presencial", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_practica_presencial"),
            )

    def test_programa_anterior_no_es_valido_horario_lab_faltante_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior.pop("semanal_lab_presencial")

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_lab_presencial", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_lab_presencial"),
            )

    def test_programa_anterior_no_es_valido_horario_teorico_practico_faltante_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior.pop("semanal_teorico_practico_presencial")

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_teorico_practico_presencial", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_teorico_practico_presencial"),
            )

    def test_programa_anterior_no_es_valido_horario_teoria_bloqueado_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior["semanal_teoria_remoto"] = 2

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_teoria_remoto", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_teoria_remoto"),
            )

    def test_programa_anterior_no_es_valido_horario_practica_bloqueado_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior["semanal_practica_remoto"] = 2

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_practica_remoto", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_practica_remoto"),
            )

    def test_programa_anterior_no_es_valido_horario_lab_bloqueado_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior["semanal_lab_remoto"] = 2

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_lab_remoto", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_lab_remoto"),
            )

    def test_programa_anterior_no_es_valido_horario_teorico_practico_bloqueado_para_metodologia(
        self,
    ):
        datos_version_anterior = {**DATOS_DEFAULT_VERSION_PROGRAMA_ASIGNATURA}
        datos_version_anterior["semanal_teorico_practico_remoto"] = 2

        datos_version_anterior["semestre"] = self.semestre_anterior
        datos_version_anterior["asignatura"] = self.asignatura
        version_anterior = VersionProgramaAsignatura.objects.create(
            **datos_version_anterior
        )

        self.__agregar_descritpores_ejes_carga_y_actividaddes(version_anterior)

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("semanal_teorico_practico_remoto", e.message_dict)
            self.assertIn(
                MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
                e.message_dict.get("semanal_teorico_practico_remoto"),
            )

    def test_programa_anterior_no_tiene_descriptores(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()

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

        # Agrego carga horaria al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
        )

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("descriptor", e.message_dict)
            self.assertIn(
                MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR, e.message_dict.get("descriptor")
            )

    def test_programa_anterior_no_tiene_ejes_transversales(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()

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

        # Agrego carga horaria al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
        )

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("eje_transversal", e.message_dict)
            self.assertIn(
                MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
                e.message_dict.get("eje_transversal"),
            )

    def test_programa_anterior_no_tiene_actividades_reservadas(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()

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

        # Agrego carga horaria al bloque
        carga_bloque = CargaBloque.objects.create(
            horas=20,
            version_programa_asignatura=version_anterior,
            bloque_curricular=self.asignatura.bloque_curricular,
        )

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("actividad_reservada", e.message_dict)
            self.assertIn(
                MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
                e.message_dict.get("actividad_reservada"),
            )

    def test_programa_anterior_no_tiene_carga_bloque(self):
        version_anterior = self.__crear_version_anterior_con_datos_default()

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

        # Agrego descriptores
        descriptores = descriptores_carrera.filter(tipo=TipoDescriptor.DESCRIPTOR)
        for descriptor in descriptores:
            ProgramaTieneDescriptor.objects.create(
                descriptor=descriptor,
                version_programa_asignatura=version_anterior,
                nivel=NivelDescriptor.BAJO,
            )

        try:
            version_nueva = (
                self.servicio_version_programa_asignatura.reutilizar_ultimo_plan(
                    self.asignatura
                )
            )
            self.assertIsNone(version_nueva, MENSAJE_SERVICIO_DEBE_FALLAR)

        except ValidationError as e:
            self.assertIn("carga_bloque", e.message_dict)
            self.assertIn(
                MENSAJE_PROGRAMA_DEBE_TENER_CARGA_HORARIA,
                e.message_dict.get("carga_bloque"),
            )

    def test_reutiliza_programa_correctamente(self):
        pass
