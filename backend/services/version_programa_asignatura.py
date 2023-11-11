import json

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

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
    MENSAJE_DESCRIPTOR_INVALIDO,
    MENSAJE_EJE_TRANSVERSAL_INVALIDO,
    MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA,
    MENSAJE_FORMATO_DESCRIPTORES_INVALIDO,
    MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO,
    MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO,
    MENSAJE_NIVEL_INVALIDO,
    MENSAJE_CAMPO_ENTERO,
)
from backend.services.semestre import ServicioSemestre
from backend.services.configuracion import ServicioConfiguracion


class ServicioVersionProgramaAsignatura:
    servicio_semestre = ServicioSemestre()
    servicio_configuracion = ServicioConfiguracion()

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

        try:
            carga_bloque = CargaBloque.objects.create(
                horas=horas,
                version_programa_asignatura=programa,
                bloque_curricular=bloque,
            )
        except (IntegrityError, ValueError) as e:
            if "horas" in str(e):
                raise ValidationError({"carga_rtf": MENSAJE_CAMPO_ENTERO})

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
                errores["descriptores"] = MENSAJE_DESCRIPTOR
            else:
                errores["ejes_transversales"] = MENSAJE_EJE_TRANSVERAL

        if len(errores.keys()) > 0:
            raise ValidationError(errores)

        programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
            descriptor=descriptor, version_programa_asignatura=programa, nivel=nivel
        )

        return programa_tiene_descriptor

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
            raise ValidationError(
                {"actividades_reservadas": MENSAJE_ACTIVIDAD_RESERVADA}
            )

        try:
            programa_tiene_actividad_reservada = (
                ProgramaTieneActividadReservada.objects.create(
                    version_programa_asignatura=programa,
                    actividad_reservada=actividad,
                    nivel=nivel,
                )
            )
        except ValueError as e:
            if "nivel" in str(e):
                raise ValidationError(
                    {"actividades_reservadas": MENSAJE_NIVEL_INVALIDO}
                )

        return programa_tiene_actividad_reservada

    def __es_posible_crear_nueva_version_de_programa(self):
        """
        Retorna verdadero si estamos dentro del periodo para crear nuevos programas, y falso sino.
        """
        return (
            self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_modificacion()
            == 0
        )

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
        resultados_de_aprendizaje: json,
    ) -> bool:
        """
        Valida los datos del programa de la asignatura para ver si cumple con las reglas del negocio
        """
        errores = {}

        # Valida los resultados de aprendizaje: Formato correcto, cantidad correcta.
        try:
            resultados = json.loads(resultados_de_aprendizaje)
        except (TypeError, json.JSONDecodeError):
            raise ValidationError(
                {"resultados_de_aprendizaje": MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO}
            )

        if not isinstance(resultados, list):
            raise ValidationError(
                {"resultados_de_aprendizaje": MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO}
            )

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

            if semanal_teoria_remoto is not None and semanal_teoria_remoto != 0:
                errores[
                    "semanal_teoria_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_practica_remoto is not None and semanal_practica_remoto != 0:
                errores[
                    "semanal_practica_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if (
                semanal_teorico_practico_remoto is not None
                and semanal_teorico_practico_remoto != 0
            ):
                errores[
                    "semanal_teorico_practico_remoto"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_lab_remoto is not None and semanal_lab_remoto != 0:
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

            if semanal_teoria_presencial is not None and semanal_teoria_presencial != 0:
                errores[
                    "semanal_teoria_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if (
                semanal_practica_presencial is not None
                and semanal_practica_presencial != 0
            ):
                errores[
                    "semanal_practica_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if (
                semanal_teorico_practico_presencial is not None
                and semanal_teorico_practico_presencial != 0
            ):
                errores[
                    "semanal_teorico_practico_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA
            if semanal_lab_presencial is not None and semanal_lab_presencial != 0:
                errores[
                    "semanal_lab_presencial"
                ] = MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA

        if len(errores.keys()) > 0:
            raise ValidationError(errores)

        return True

    def crear_nueva_version_programa_asignatura(
        self,
        asignatura: Asignatura,
        descriptores: list,  # Solo los ID de los descriptores, porque es si o no.
        actividades_reservadas: list,
        ejes_transversales: list,
        carga_rtf: int,
        resultados_de_aprendizaje: json,
        semanas_dictado: int,
        contenidos: str,
        bibliografia: str,
        recursos: str,
        evaluacion: str,
        investigacion_docentes: str,
        investigacion_estudiantes: str,
        extension_docentes: str,
        extension_estudiantes: str,
        cronograma: str,
        semanal_teoria_presencial: int = 0,
        semanal_practica_presencial: int = 0,
        semanal_teorico_practico_presencial: int = 0,
        semanal_lab_presencial: int = 0,
        semanal_teoria_remoto: int = 0,
        semanal_practica_remoto: int = 0,
        semanal_teorico_practico_remoto: int = 0,
        semanal_lab_remoto: int = 0,
    ):
        if not self.__es_posible_crear_nueva_version_de_programa():
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        semestre = self.servicio_semestre.obtener_semestre_siguiente()

        mensajes_de_error = {}
        if len(descriptores) == 0:
            mensajes_de_error["descriptores"] = MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR
        if len(actividades_reservadas) == 0:
            mensajes_de_error[
                "actividades_reservadas"
            ] = MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA
        if len(ejes_transversales) == 0:
            mensajes_de_error[
                "ejes_transversales"
            ] = MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL

        if len(mensajes_de_error.keys()) > 0:
            raise ValidationError(mensajes_de_error)

        # Obtengo todos los descriptores
        # La lista de descriptores tiene el siguiente formato:
        # {
        #   "id": int
        # }

        # Creo una lista de los id de los descriptores asi hago un bulk filter.
        try:
            id_descriptores = [descriptor["id"] for descriptor in descriptores]
        except (TypeError, KeyError):
            raise ValidationError(
                {"descriptores": MENSAJE_FORMATO_DESCRIPTORES_INVALIDO}
            )

        instancias_descriptores = Descriptor.objects.filter(
            id__in=id_descriptores, tipo=TipoDescriptor.DESCRIPTOR
        )

        if len(descriptores) != len(instancias_descriptores):
            raise ValidationError({"descriptores": MENSAJE_DESCRIPTOR_INVALIDO})

        # Validar datos:
        if self.__validar_datos(
            asignatura=asignatura,
            semanal_teoria_presencial=semanal_teoria_presencial,
            semanal_lab_presencial=semanal_lab_presencial,
            semanal_lab_remoto=semanal_lab_remoto,
            semanal_practica_presencial=semanal_practica_presencial,
            semanal_practica_remoto=semanal_practica_remoto,
            semanal_teoria_remoto=semanal_teoria_remoto,
            semanal_teorico_practico_presencial=semanal_teorico_practico_presencial,
            semanal_teorico_practico_remoto=semanal_teorico_practico_remoto,
            resultados_de_aprendizaje=resultados_de_aprendizaje,
        ):
            with transaction.atomic():
                # Creo un programa. Si falla algo, saltara una excepcion
                try:
                    version_programa = VersionProgramaAsignatura(
                        estado=EstadoAsignatura.ABIERTO,
                        asignatura=asignatura,
                        semestre=semestre,
                        semanas_dictado=semanas_dictado,
                        semanal_teoria_presencial=semanal_teoria_presencial,
                        semanal_practica_presencial=semanal_practica_presencial,
                        semanal_teorico_practico_presencial=semanal_teorico_practico_presencial,
                        semanal_lab_presencial=semanal_lab_presencial,
                        semanal_teoria_remoto=semanal_teoria_remoto,
                        semanal_practica_remoto=semanal_practica_remoto,
                        semanal_teorico_practico_remoto=semanal_teorico_practico_remoto,
                        semanal_lab_remoto=semanal_lab_remoto,
                        resultados_de_aprendizaje=resultados_de_aprendizaje,
                        contenidos=contenidos,
                        bibliografia=bibliografia,
                        recursos=recursos,
                        evaluacion=evaluacion,
                        investigacion_docentes=investigacion_docentes,
                        investigacion_estudiantes=investigacion_estudiantes,
                        extension_docentes=extension_docentes,
                        extension_estudiantes=extension_estudiantes,
                        cronograma=cronograma,
                    )
                    version_programa.full_clean()
                    version_programa.save()
                except (ValueError, IntegrityError) as e:
                    mensajes_de_error = {
                        "semanal_teoria_presencial": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_practica_presencial": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_teorico_practico_presencial": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_lab_presencial": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_teoria_remoto": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_practica_remoto": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_teorico_practico_remoto": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanal_lab_remoto": MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA,
                        "semanas_dictado": MENSAJE_CAMPO_ENTERO,
                    }

                    for campo, mensaje in mensajes_de_error.items():
                        if campo in str(e):
                            raise ValidationError({campo: mensaje})

                for descriptor in instancias_descriptores:
                    self.__asignar_descriptor(
                        descriptor, version_programa, NivelDescriptor.BAJO
                    )

                # Obtengo todos los ejes transversales
                # La lista de ejes transversales tiene el siguiente formato:
                # {
                #   "id": int,
                #   "nivel": int
                # }

                for eje in ejes_transversales:
                    try:
                        instancia_eje_transversal = Descriptor.objects.get(
                            id=eje["id"], tipo=TipoDescriptor.EJE_TRANSVERSAL
                        )
                        self.__asignar_descriptor(
                            instancia_eje_transversal, version_programa, eje["nivel"]
                        )
                    except Descriptor.DoesNotExist:
                        raise ValidationError(
                            {"ejes_transversales": MENSAJE_EJE_TRANSVERSAL_INVALIDO}
                        )
                    except (TypeError, KeyError, ValueError):
                        raise ValidationError(
                            {
                                "ejes_transversales": MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO
                            }
                        )

                # Obtengo todas las actividades reservadas
                # La lista de actividades reservadas tiene el siguiente formato:
                # {
                #   "id": int,
                #   "nivel": int
                # }

                for actividad in actividades_reservadas:
                    try:
                        instancia_actividad_reservada = ActividadReservada.objects.get(
                            id=actividad["id"]
                        )
                        self.__asignar_actividad_reservada(
                            instancia_actividad_reservada,
                            version_programa,
                            actividad["nivel"],
                        )
                    except ActividadReservada.DoesNotExist:
                        raise ValidationError(
                            {
                                "actividades_reservadas": MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA
                            }
                        )
                    except (TypeError, KeyError, ValueError):
                        raise ValidationError(
                            {
                                "actividades_reservadas": MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO
                            }
                        )

                # Carga del bloque
                self.__asignar_carga_horaria(
                    asignatura.bloque_curricular, version_programa, carga_rtf
                )

            return version_programa

    def modificar_version_programa_asignatura(
        self, version_programa: VersionProgramaAsignatura, **args
    ):
        pass

    def presentar_programa_para_aprobacion(self, programa: VersionProgramaAsignatura):
        pass

    def reutilizar_ultimo_plan(self, asignatura: Asignatura):
        """
        Toma la ultima version del plan de la asignatura, y crea una nueva con los mismos datos.
        """

        if not self.__es_posible_crear_nueva_version_de_programa():
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        semestre_actual = self.servicio_semestre.obtener_semestre_actual()

        try:
            ultimo_programa = VersionProgramaAsignatura.objects.get(
                asignatura=asignatura
            )

        except VersionProgramaAsignatura.DoesNotExist:
            raise ValidationError({"asignatura": MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES})

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
                {
                    "actividades_reservadas": MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA
                }
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

        return nuevo_programa
