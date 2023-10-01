import json

from django.core.exceptions import ValidationError
from django.db import transaction

from backend.models import (
    BloqueCurricular,
    CargaBloque,
    VersionProgramaAsignatura,
    Asignatura,
    Descriptor,
    ActividadReservada,
    PlanDeEstudio,
    Estandar,
    ProgramaTieneDescriptor,
    ProgramaTieneActividadReservada,
    Semestre,
)
from backend.common.choices import (
    NivelDescriptor,
    MetodologiaAsignatura,
    TipoDescriptor,
    EstadoAsignatura,
)
from backend.common.constantes import (
    MINIMO_RESULTADOS_DE_APRENDIZAJE,
    MAXIMO_RESULTADOS_DE_APRENDIZAJE,
)
from backend.common.mensajes_de_error import (
    MENSAJE_EJE_TRANSVERAL,
    MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO,
    MENSAJE_CANTIDAD_DE_RESULTADOS,
    MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
    MENSAJE_ACTIVIDAD_RESERVADA,
    MENSAJE_NIVEL_INCORRECTO,
    MENSAJE_DESCRIPTOR,
    MENSAJE_BLOQUE_CURRICUALR,
    MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES,
    MENSAJE_PROGRAMAS_CERRADOS,
    MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA,
    MENSAJE_VERSION_ANTERIOR_NO_APROBADA,
    MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
    MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR,
    MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
    MENSAJE_PROGRAMA_DEBE_TENER_CARGA_HORARIA,
)


class ServicioVersionProgramaAsignatura:
    def __asignar_carga_horaria(
        self, bloque: BloqueCurricular, programa: VersionProgramaAsignatura, horas: int
    ) -> CargaBloque:
        """
        Asigna a una version de programa una carga horaria para un determinado bloque curricular.
        Verifica que la asignatura relacionada al programa tenga el mismo bloque curricular que el referenciado.

        Tira ValidationError cuando falla la validacion, con codigos de error: "bloque", "programa", "carga"
        """

        if programa.asignatura.bloque_curricular != bloque:
            raise ValidationError({"bloque_curricular": MENSAJE_BLOQUE_CURRICUALR})

        carga_bloque = CargaBloque.objects.create(
            horas=horas, version_programa_asignatura=programa, bloque_curricular=bloque
        )

        return carga_bloque

    def __asignar_descriptor(
        self,
        descriptor: Descriptor,
        programa: VersionProgramaAsignatura,
        nivel: NivelDescriptor,
    ) -> ProgramaTieneDescriptor:
        """
        Asigna descriptor para un cierto programa de asignatura. Verifica que el descriptor seleccionado
        pertenezca al estandar de alguna de las carreras que tienen la asignatura.
        Ademas, verifica el tipo de descriptor segun el nivel.
        """
        errores = {}

        # Primero valida el nivel
        if descriptor.tipo == TipoDescriptor.DESCRIPTOR:
            if nivel == NivelDescriptor.MEDIO or nivel == NivelDescriptor.ALTO:
                errores["nivel"] = MENSAJE_NIVEL_INCORRECTO

        estandares_descriptor = Estandar.objects.filter(descriptores__in=[descriptor])
        planes_de_estudio_asignatura = PlanDeEstudio.objects.filter(
            asignaturas__in=[programa.asignatura]
        )

        carreras = []

        for plan in planes_de_estudio_asignatura:
            carreras.append(plan.carrera)

        carrera_descriptor_coincide_con_programa = False
        for estandar in estandares_descriptor:
            if estandar.carrera in carreras:
                carrera_descriptor_coincide_con_programa = True

        if not carrera_descriptor_coincide_con_programa:
            if descriptor.tipo == TipoDescriptor.DESCRIPTOR:
                errores["descriptor"] = MENSAJE_DESCRIPTOR
            else:
                errores["eje_transversal"] = MENSAJE_EJE_TRANSVERAL

        if len(errores.keys()) > 0:
            raise ValidationError(errores)

        programa_tiene_dessciptor = ProgramaTieneDescriptor.objects.create(
            descriptor=descriptor, version_programa_asignatura=programa, nivel=nivel
        )

        return programa_tiene_dessciptor

    def __asignar_actividad_reservada(
        self,
        actividad: ActividadReservada,
        programa: VersionProgramaAsignatura,
        nivel: NivelDescriptor,
    ) -> ProgramaTieneActividadReservada:
        """
        Asigna una actividad reservada para cierto programa de asignatura. Verifica que la actividad seleccionada
        pertenezca al estandar de alguna de las carreras que tienen la asignatura.
        """

        estandar_actividad = actividad.estandar
        carrera_actividad = estandar_actividad.carrera

        planes_de_estudio = PlanDeEstudio.objects.filter(
            asignaturas__in=[programa.asignatura]
        )

        carrera_actividad_coincide_con_programas = False
        for plan in planes_de_estudio:
            if plan.carrera == carrera_actividad:
                carrera_actividad_coincide_con_programas = True

        if not carrera_actividad_coincide_con_programas:
            raise ValidationError({"actividad_reservada": MENSAJE_ACTIVIDAD_RESERVADA})

        programa_tiene_actividad_reservada = (
            ProgramaTieneActividadReservada.objects.create(
                version_programa_asignatura=programa,
                actividad_reservada=actividad,
                nivel=nivel,
            )
        )

        return programa_tiene_actividad_reservada

    def __es_posible_crear_nueva_version_de_programa(self):
        """
        Retorna verdadero si estamos dentro del periodo para crear nuevos programas, y falso sino.
        """

        # TODO. Hacer este servicio
        return True

    def __validar_datos(
        self,
        asignatura: Asignatura,
        semanal_teoria_presencial: int,
        semanal_practica_presencial: int,
        semanal_teorico_practico_presencial: int,
        semanal_lab_presencial: int,
        semanal_teoria_remoto: int,
        semanal_practica_remoto: int,
        semanal_teorico_practico_remoto: int,
        semanal_lab_remoto: int,
        resultados_de_aprendizaje,
    ) -> bool:
        """
        Valida los datos del programa de la asignatura para ver si cumple con las reglas del negocio
        """
        errores = {}

        # Valida los resultados de aprendizaje: Formato correcto, cantidad correcta.
        resultados = json.loads(resultados_de_aprendizaje)

        if not isinstance(resultados, list):
            errores[
                "resultados_de_aprendizaje"
            ] = MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO

        if (
            len(resultados) < MINIMO_RESULTADOS_DE_APRENDIZAJE
            or len(resultados) > MAXIMO_RESULTADOS_DE_APRENDIZAJE
        ):
            errores["resultados_de_aprendizaje"] = MENSAJE_CANTIDAD_DE_RESULTADOS

        # Valida los horarios dependiendo la metodologia de la asignatura.
        if (
            asignatura.metodologia == MetodologiaAsignatura.PRESENCIAL
            or asignatura.metodologia == MetodologiaAsignatura.HIBRIDO
        ):
            if semanal_teoria_presencial is None:
                errores[
                    "semanal_teoria_presencial"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA
            if semanal_practica_presencial is None:
                errores[
                    "semanal_practica_presencial"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA
            if semanal_teorico_practico_presencial is None:
                errores[
                    "semanal_teorico_practico_presencial"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA
            if semanal_lab_presencial is None:
                errores[
                    "semanal_lab_presencial"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA

            if semanal_teoria_remoto is not None:
                errores[
                    "semanal_teoria_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_practica_remoto is not None:
                errores[
                    "semanal_practica_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_teorico_practico_remoto is not None:
                errores[
                    "semanal_teorico_practico_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_lab_remoto is not None:
                errores[
                    "semanal_lab_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA

        if (
            asignatura.metodologia == MetodologiaAsignatura.VIRTUAL
            or asignatura.metodologia == MetodologiaAsignatura.HIBRIDO
        ):
            if semanal_teoria_remoto is None:
                errores[
                    "semanal_teoria_remoto"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA
            if semanal_practica_remoto is None:
                errores[
                    "semanal_practica_remoto"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA
            if semanal_teorico_practico_remoto is None:
                errores[
                    "semanal_teorico_practico_remoto"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA
            if semanal_lab_remoto is None:
                errores[
                    "semanal_lab_remoto"
                ] = MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA

            if semanal_teoria_presencial is not None:
                errores[
                    "semanal_teoria_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_practica_presencial is not None:
                errores[
                    "semanal_practica_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_teorico_practico_presencial is not None:
                errores[
                    "semanal_teorico_practico_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_lab_presencial is not None:
                errores[
                    "semanal_lab_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA

        if len(errores.keys()) > 0:
            raise ValidationError(errores)

        return True

    def crear_nueva_version_programa_asignatura(self, semestre: Semestre, **args):
        # TODO. verificar si estamos en periodo de poder crear una nueva version del programa de la asignatura.
        pass

    def modificar_version_programa_asignatura(self, **args):
        pass

    def presentar_programa_para_aprobacion(self, programa: VersionProgramaAsignatura):
        pass

    def reutilizar_ultimo_plan(self, asignatura: Asignatura):
        """
        Toma la ultima version del plan de la asignatura, y crea una nueva con los mismos datos y presenta para aprobacion.
        """

        if not self.__es_posible_crear_nueva_version_de_programa():
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        ultimos_programas = VersionProgramaAsignatura.objects.filter(
            asignatura=asignatura
        )

        if not ultimos_programas.exists():
            raise ValidationError({"asignatura": MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES})

        ultimo_programa: VersionProgramaAsignatura = ultimos_programas.latest(
            "creado_en"
        )

        if ultimo_programa.estado != EstadoAsignatura.APROBADO:
            raise ValidationError({"asignatura": MENSAJE_VERSION_ANTERIOR_NO_APROBADA})

        descriptores_del_programa = ProgramaTieneDescriptor.objects.filter(
            version_programa_asignatura=ultimo_programa
        )

        descriptores = descriptores_del_programa.filter(
            descriptor__tipo=TipoDescriptor.DESCRIPTOR
        )
        ejes = descriptores_del_programa.filter(
            descriptor__tipo=TipoDescriptor.EJE_TRANSVERSAL
        )

        if not descriptores.exists():
            raise ValidationError(
                {"descriptor": MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR}
            )

        if not ejes.exists():
            raise ValidationError(
                {"eje_transversal": MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL}
            )

        actividades_reservadas = ProgramaTieneActividadReservada.objects.filter(
            version_programa_asignatura=ultimo_programa
        )
        if not actividades_reservadas.exists():
            raise ValidationError(
                {"actividad_reservada": MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA}
            )

        # Asi si alguna falla, que no se guarde nada. Esta bien?
        with transaction.atomic():
            if self.__validar_datos(
                asignatura=ultimo_programa.asignatura,
                semanal_teoria_presencial=ultimo_programa.semanal_teoria_presencial,
                semanal_practica_presencial=ultimo_programa.semanal_practica_presencial,
                semanal_teorico_practico_presencial=ultimo_programa.semanal_teorico_practico_presencial,
                semanal_lab_presencial=ultimo_programa.semanal_lab_presencial,
                semanal_teoria_remoto=ultimo_programa.semanal_teoria_remoto,
                semanal_practica_remoto=ultimo_programa.semanal_practica_remoto,
                semanal_teorico_practico_remoto=ultimo_programa.semanal_teorico_practico_remoto,
                semanal_lab_remoto=ultimo_programa.semanal_lab_remoto,
                resultados_de_aprendizaje=ultimo_programa.resultados_de_aprendizaje,
            ):
                nuevo_programa = VersionProgramaAsignatura.objects.create(
                    asignatura=ultimo_programa.asignatura,
                    semestre=ultimo_programa.semestre,
                    estado=EstadoAsignatura.ABIERTO,
                    semanas_dictado=ultimo_programa.semanas_dictado,
                    semanal_teoria_presencial=ultimo_programa.semanal_teoria_presencial,
                    semanal_practica_presencial=ultimo_programa.semanal_practica_presencial,
                    semanal_teorico_practico_presencial=ultimo_programa.semanal_teorico_practico_presencial,
                    semanal_lab_presencial=ultimo_programa.semanal_lab_presencial,
                    semanal_teoria_remoto=ultimo_programa.semanal_teoria_remoto,
                    semanal_practica_remoto=ultimo_programa.semanal_practica_remoto,
                    semanal_teorico_practico_remoto=ultimo_programa.semanal_teorico_practico_remoto,
                    semanal_lab_remoto=ultimo_programa.semanal_lab_remoto,
                    contenidos=ultimo_programa.contenidos,
                    bibliografia=ultimo_programa.bibliografia,
                    recursos=ultimo_programa.recursos,
                    evaluacion=ultimo_programa.evaluacion,
                    investigacion_docentes=ultimo_programa.investigacion_docentes,
                    investigacion_estudiantes=ultimo_programa.investigacion_estudiantes,
                    extension_docentes=ultimo_programa.extension_docentes,
                    extension_estudiantes=ultimo_programa.extension_docentes,
                    cronograma=ultimo_programa.cronograma,
                    resultados_de_aprendizaje=ultimo_programa.resultados_de_aprendizaje,
                )

            for descriptor_del_programa in descriptores_del_programa:
                self.__asignar_descriptor(
                    descriptor=descriptor_del_programa.descriptor,
                    programa=nuevo_programa,
                    nivel=descriptor_del_programa.nivel,
                )
            for actividad_reservada in actividades_reservadas:
                self.__asignar_actividad_reservada(
                    actividad=actividad_reservada.actividad_reservada,
                    programa=nuevo_programa,
                    nivel=actividad_reservada.nivel,
                )

            try:
                carga_bloque_programa = CargaBloque.objects.get(
                    version_programa_asignatura=ultimo_programa
                )

            except CargaBloque.DoesNotExist:
                raise ValidationError(
                    {"carga_bloque": MENSAJE_PROGRAMA_DEBE_TENER_CARGA_HORARIA}
                )

            self.__asignar_carga_horaria(
                bloque=carga_bloque_programa.bloque_curricular,
                programa=nuevo_programa,
                horas=carga_bloque_programa.horas,
            )

        self.presentar_programa_para_aprobacion(nuevo_programa)
        return nuevo_programa
