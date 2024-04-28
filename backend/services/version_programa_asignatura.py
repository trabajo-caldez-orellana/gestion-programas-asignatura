import json
from typing import Optional, List

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet, Q
from django.conf import settings

from backend.models import (
    VersionProgramaAsignatura,
    Asignatura,
    Descriptor,
    ActividadReservada,
    PlanDeEstudio,
    Estandar,
    ProgramaTieneDescriptor,
    ProgramaTieneActividadReservada,
    Rol,
    Carrera,
    Semestre,
    AuditoriaEstadoVersionPrograma,
    Correlativa,
)
from backend.common.choices import (
    NivelDescriptor,
    TipoDescriptor,
    EstadoAsignatura,
    Roles,
    Semestres,
    EstadosAprobacionPrograma,
    TiposDeEmail,
    TipoCorrelativa,
    RequisitosCorrelativa,
)
from backend.common.constantes import (
    MINIMO_RESULTADOS_DE_APRENDIZAJE,
    MAXIMO_RESULTADOS_DE_APRENDIZAJE,
)
from backend.common.mensajes_de_error import (
    MENSAJE_EJE_TRANSVERAL,
    MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO,
    MENSAJE_CANTIDAD_DE_RESULTADOS,
    MENSAJE_ACTIVIDAD_RESERVADA,
    MENSAJE_NIVEL_INCORRECTO,
    MENSAJE_DESCRIPTOR,
    MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES,
    MENSAJE_PROGRAMAS_CERRADOS,
    MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL,
    MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR,
    MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA,
    MENSAJE_DESCRIPTOR_INVALIDO,
    MENSAJE_EJE_TRANSVERSAL_INVALIDO,
    MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA,
    MENSAJE_FORMATO_DESCRIPTORES_INVALIDO,
    MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO,
    MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO,
    MENSAJE_NIVEL_INVALIDO,
    MENSAJE_VERSION_CERRADA_PARA_MODIFICACION,
    MENSAJE_PROGRAMA_YA_EXISTENTE,
    MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR,
    MENSAJE_FALLO_REUTILIZACION,
    MENSAJE_PROGRAMA_NO_SE_ENCUENTRA_DISPONIBLE_PARA_CORREGIR,
    MENSAJE_REQUISITO_CORRELATIVA_INVALIDO,
    MENSAJE_TIPO_CORRELATIVA_INVALIDO,
    MENSAJE_ASIGNATURA_NECESARIA,
    MENSAJE_CANTIDAD_ASIGNATURAS_NECESARIA,
    MENSAJE_MODULO_NECESARIO,
    MENSAJE_CORRELATIVA_INVALIDA,
)
from backend.services.semestre import ServicioSemestre
from backend.services.configuracion import ServicioConfiguracion
from backend.services.plan_de_estudio import ServicioPlanDeEstudio
from backend.serializers import SerializerAsignatura
from backend.common.funciones_fecha import obtener_fecha_y_hora_actual
from backend.tasks import enviar_email_async


class ServicioVersionProgramaAsignatura:
    """
    Todos los servicios relacionados a la creacion, modificacion, y seguimiento de los Programas
    de asignatura
    """

    servicio_semestre = ServicioSemestre()
    servicio_configuracion = ServicioConfiguracion()
    servicio_planes = ServicioPlanDeEstudio()

    def _es_nivel_descriptor_valido(
        self, descriptor: Descriptor, nivel: NivelDescriptor
    ):
        if descriptor.tipo == TipoDescriptor.DESCRIPTOR:
            if nivel != NivelDescriptor.BAJO and nivel != NivelDescriptor.NADA:
                return False
        return True

    def _asignar_o_modificar_descriptor_prograna(
        self,
        descriptor: Descriptor,
        programa: VersionProgramaAsignatura,
        nivel: NivelDescriptor,
        asignacion: ProgramaTieneDescriptor = None,
    ) -> ProgramaTieneDescriptor:
        """
        Asigna descriptor para un cierto programa de asignatura. Verifica que el descriptor seleccionado
        pertenezca al estandar de alguna de las carreras que tienen la asignatura.
        Ademas, verifica el tipo de descriptor segun el nivel.
        """
        errores = {}

        # Primero valida el nivel
        if not self._es_nivel_descriptor_valido(descriptor, nivel):
            errores["descriptores"] = MENSAJE_NIVEL_INCORRECTO

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

        try:
            if asignacion is None:
                programa_tiene_descriptor = ProgramaTieneDescriptor.objects.create(
                    descriptor=descriptor,
                    version_programa_asignatura=programa,
                    nivel=nivel,
                )
            else:
                asignacion.nivel = nivel
                asignacion.full_clean()
                asignacion.save()
                programa_tiene_descriptor = asignacion
        except (ValueError, ValidationError) as e:
            if "nivel" in str(e):
                if descriptor.tipo == TipoDescriptor.DESCRIPTOR:
                    raise ValidationError(
                        {"descriptores": MENSAJE_NIVEL_INVALIDO}
                    ) from e
                else:
                    raise ValidationError(
                        {"ejes_transversales": MENSAJE_NIVEL_INVALIDO}
                    ) from e
        return programa_tiene_descriptor

    def _asignar_o_modificar_nivel_actividad_reservada(
        self,
        actividad: ActividadReservada,
        programa: VersionProgramaAsignatura,
        nivel: NivelDescriptor,
        asignacion: ProgramaTieneActividadReservada = None,
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
            if asignacion is None:
                programa_tiene_actividad_reservada = (
                    ProgramaTieneActividadReservada.objects.create(
                        version_programa_asignatura=programa,
                        actividad_reservada=actividad,
                        nivel=nivel,
                    )
                )
            else:
                asignacion.nivel = nivel
                asignacion.full_clean()
                asignacion.save()
                programa_tiene_actividad_reservada = asignacion
        except (ValueError, ValidationError) as e:
            if "nivel" in str(e):
                raise ValidationError(
                    {"actividades_reservadas": MENSAJE_NIVEL_INVALIDO}
                ) from e

        return programa_tiene_actividad_reservada

    def _asignar_o_modificar_correlativa(
        self,
        version_programa_asignatura: VersionProgramaAsignatura,
        objeto_correlativa: object,
        instancia_correlativa: Optional[Correlativa] = None,
    ):
        try:
            tipo = objeto_correlativa["tipo"]
        except Exception:
            raise ValidationError({"correlativas": MENSAJE_TIPO_CORRELATIVA_INVALIDO})

        try:
            requisito = objeto_correlativa["requisito"]
        except Exception:
            raise ValidationError(
                {"correlativas": MENSAJE_REQUISITO_CORRELATIVA_INVALIDO}
            )

        if tipo != TipoCorrelativa.APROBADO and tipo != TipoCorrelativa.REGULAR:
            raise ValidationError({"correlativas": MENSAJE_TIPO_CORRELATIVA_INVALIDO})

        if requisito == RequisitosCorrelativa.ASIGNATURA:
            try:
                asignatura = objeto_correlativa["asignatura_correlativa"]

                if asignatura is None:
                    raise ValidationError(
                        {"correlativas": MENSAJE_ASIGNATURA_NECESARIA}
                    )

                instancia_asignatura = Asignatura.objects.get(id=asignatura["id"])

                if instancia_correlativa is None:
                    correlativa_nueva = Correlativa(
                        version_programa_asignatura=version_programa_asignatura,
                        asignatura_correlativa=instancia_asignatura,
                        tipo=tipo,
                        requisito=RequisitosCorrelativa.ASIGNATURA,
                    )
                    correlativa_nueva.full_clean()
                    correlativa_nueva.save()
                else:
                    instancia_correlativa.tipo = tipo
                    instancia_correlativa.requisito = RequisitosCorrelativa.ASIGNATURA
                    instancia_correlativa.asignatura_correlativa = instancia_asignatura
                    instancia_correlativa.full_clean()
                    instancia_correlativa.save()

            except Exception:
                raise ValidationError({"correlativas": MENSAJE_ASIGNATURA_NECESARIA})

        elif requisito == RequisitosCorrelativa.CANTIDAD_ASIGNATURAS:
            try:
                cantidad_asignaturas = objeto_correlativa["cantidad_asignaturas"]
                if cantidad_asignaturas is None or cantidad_asignaturas == 0:
                    raise ValidationError(
                        {"correlativas": MENSAJE_CANTIDAD_ASIGNATURAS_NECESARIA}
                    )

                if instancia_correlativa is None:
                    correlativa_nueva = Correlativa(
                        version_programa_asignatura=version_programa_asignatura,
                        cantidad_asignaturas=cantidad_asignaturas,
                        tipo=tipo,
                        requisito=RequisitosCorrelativa.CANTIDAD_ASIGNATURAS,
                    )
                    correlativa_nueva.full_clean()
                    correlativa_nueva.save()
                else:
                    instancia_correlativa.tipo = tipo
                    instancia_correlativa.requisito = (
                        RequisitosCorrelativa.CANTIDAD_ASIGNATURAS
                    )
                    instancia_correlativa.cantidad_asignaturas = cantidad_asignaturas
                    instancia_correlativa.full_clean()
                    instancia_correlativa.save()

            except Exception:
                raise ValidationError(
                    {"correlativas": MENSAJE_CANTIDAD_ASIGNATURAS_NECESARIA}
                )
        elif requisito == RequisitosCorrelativa.MODULO:
            try:
                modulo = objeto_correlativa["modulo"]
                if modulo is None or modulo == "":
                    raise ValidationError({"correlativas": MENSAJE_MODULO_NECESARIO})

                if instancia_correlativa is None:
                    correlativa_nueva = Correlativa(
                        version_programa_asignatura=version_programa_asignatura,
                        modulo=modulo,
                        tipo=tipo,
                        requisito=RequisitosCorrelativa.MODULO,
                    )
                    correlativa_nueva.full_clean()
                    correlativa_nueva.save()
                else:
                    instancia_correlativa.tipo = tipo
                    instancia_correlativa.requisito = RequisitosCorrelativa.MODULO
                    instancia_correlativa.modulo = modulo
                    instancia_correlativa.full_clean()
                    instancia_correlativa.save()

            except Exception:
                raise ValidationError({"correlativas": MENSAJE_MODULO_NECESARIO})
        else:
            raise ValidationError(
                {"correlativas": MENSAJE_REQUISITO_CORRELATIVA_INVALIDO}
            )

    def _es_posible_crear_nueva_version_de_programa(
        self, semestre_asignatura: Semestres
    ):
        """
        Retorna verdadero si estamos dentro del periodo para crear nuevos programas, y falso sino.
        """

        try:
            return (
                self.servicio_configuracion.obtener_dias_restantes_inicio_periodo_modificacion(
                    semestre_asignatura
                )
                == 0
            )
        except ValidationError:
            return False

    def _validar_resultados_de_aprendizaje(
        self,
        resultados_de_aprendizaje: json,
    ) -> bool:
        """
        Valida los datos del programa de la asignatura para ver si cumple con las reglas del negocio
        """
        # Valida los resultados de aprendizaje: Formato correcto, cantidad correcta.
        resultados = json.loads(resultados_de_aprendizaje)
        if not isinstance(resultados, list):
            raise ValidationError(
                {"resultados_de_aprendizaje": MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO}
            )

        if (
            len(resultados) < MINIMO_RESULTADOS_DE_APRENDIZAJE
            or len(resultados) > MAXIMO_RESULTADOS_DE_APRENDIZAJE
        ):
            raise ValidationError(
                {"resultados_de_aprendizaje": MENSAJE_CANTIDAD_DE_RESULTADOS}
            )

        return True

    def _el_programa_ya_existe(
        self, asignatura: Asignatura, semestre: Semestre
    ) -> bool:
        programas_count = VersionProgramaAsignatura.objects.filter(
            asignatura_id=asignatura.id, semestre_id=semestre.id
        ).count()
        return programas_count > 0

    def crear_nueva_version_programa_asignatura(
        self,
        asignatura: Asignatura,
        descriptores: list,  # Solo los ID de los descriptores, porque es si o no.
        actividades_reservadas: list,
        ejes_transversales: list,
        resultados_de_aprendizaje: List[str],
        contenidos: str,
        bibliografia: str,
        recursos: str,
        evaluacion: str,
        investigacion_docentes: str,
        investigacion_estudiantes: str,
        metodologia_aplicada: str,
        fundamentacion: str,
        extension_docentes: str,
        extension_estudiantes: str,
        cronograma: str,
        correlativas: list,
    ):
        """
        Crea una nueva version de un programa de asignatura para el semestre que viene!
        """
        if not self._es_posible_crear_nueva_version_de_programa(
            asignatura.semestre_dictado
        ):
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        semestre = self.servicio_semestre.obtener_semestre_siguiente()

        if self._el_programa_ya_existe(asignatura, semestre):
            raise ValidationError({"__all__": MENSAJE_PROGRAMA_YA_EXISTENTE})

        # Obtengo todos los descriptores
        # La lista de descriptores tiene el siguiente formato:
        # {
        #   "id": int
        # }

        # Creo una lista de los id de los descriptores asi hago un bulk filter.
        try:
            id_descriptores = [descriptor["id"] for descriptor in descriptores]
        except (TypeError, KeyError) as exc:
            raise ValidationError(
                {"descriptores": MENSAJE_FORMATO_DESCRIPTORES_INVALIDO}
            ) from exc

        instancias_descriptores = Descriptor.objects.filter(
            id__in=id_descriptores, tipo=TipoDescriptor.DESCRIPTOR
        )

        if len(descriptores) != len(instancias_descriptores):
            raise ValidationError({"descriptores": MENSAJE_DESCRIPTOR_INVALIDO})

        # Validar datos:
        if self._validar_resultados_de_aprendizaje(
            resultados_de_aprendizaje=resultados_de_aprendizaje,
        ):
            with transaction.atomic():
                # Creo un programa. Si falla algo, saltara una excepcion
                resultados = json.loads(resultados_de_aprendizaje)
                version_programa = VersionProgramaAsignatura(
                    estado=EstadoAsignatura.ABIERTO,
                    asignatura=asignatura,
                    semestre=semestre,
                    resultados_de_aprendizaje=resultados,
                    contenidos=contenidos,
                    bibliografia=bibliografia,
                    recursos=recursos,
                    evaluacion=evaluacion,
                    investigacion_docentes=investigacion_docentes,
                    investigacion_estudiantes=investigacion_estudiantes,
                    extension_docentes=extension_docentes,
                    extension_estudiantes=extension_estudiantes,
                    metodologia_aplicada=metodologia_aplicada,
                    fundamentacion=fundamentacion,
                    cronograma=cronograma,
                )
                version_programa.full_clean()
                version_programa.save()

                for descriptor in instancias_descriptores:
                    self._asignar_o_modificar_descriptor_prograna(
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
                        self._asignar_o_modificar_descriptor_prograna(
                            instancia_eje_transversal, version_programa, eje["nivel"]
                        )
                    except Descriptor.DoesNotExist as exc:
                        raise ValidationError(
                            {"ejes_transversales": MENSAJE_EJE_TRANSVERSAL_INVALIDO}
                        ) from exc
                    except (TypeError, KeyError, ValueError) as exc:
                        raise ValidationError(
                            {
                                "ejes_transversales": MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO
                            }
                        ) from exc

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
                        self._asignar_o_modificar_nivel_actividad_reservada(
                            instancia_actividad_reservada,
                            version_programa,
                            actividad["nivel"],
                        )
                    except ActividadReservada.DoesNotExist as exc:
                        raise ValidationError(
                            {
                                "actividades_reservadas": MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA
                            }
                        ) from exc
                    except (TypeError, KeyError, ValueError) as exc:
                        raise ValidationError(
                            {
                                "actividades_reservadas": MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO
                            }
                        ) from exc

                # Obtengo todas las correlativas
                # La lista de correlativas tiene el siguiente formato:
                # {
                #   "id": int | None,
                #   "tipo": TipoCorrelativa,
                #   "requisito": RequisitoCorrelativa,
                #   "cantidadAsignaturas": int | None
                #   "asignatura": {
                #     "id": int,
                #     "informacion": str
                #   } | None,
                #   "modulo": str | None
                # }

                for correlativa in correlativas:
                    self._asignar_o_modificar_correlativa(
                        version_programa_asignatura=version_programa,
                        objeto_correlativa=correlativa,
                    )

            return version_programa

    def modificar_version_programa_asignatura(
        self,
        version_programa: VersionProgramaAsignatura,
        descriptores: list,
        actividades_reservadas: list,
        ejes_transversales: list,
        resultados_de_aprendizaje: json,
        contenidos: str,
        bibliografia: str,
        metodologia_aplicada: str,
        fundamentacion: str,
        recursos: str,
        evaluacion: str,
        investigacion_docentes: str,
        investigacion_estudiantes: str,
        extension_docentes: str,
        extension_estudiantes: str,
        correlativas: list,
        cronograma: str,
    ):
        """
        Modifica la version de un programa de asignatura para el semestre que viene!
        Verifica que sea periodo de modificacion de programas
        """
        # Verifica el estado de la version del programa de la asignatura

        if version_programa.estado != EstadoAsignatura.ABIERTO:
            raise ValidationError(
                {"__all__": MENSAJE_VERSION_CERRADA_PARA_MODIFICACION}
            )

        # Deberia ser periodo de modificacion?
        if not self._es_posible_crear_nueva_version_de_programa(
            version_programa.asignatura.semestre_dictado
        ):
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        # Formato descriptores, actividades y ejes transversales:
        # {
        #  "id": number,
        #  "seleccionado": boolean
        # }

        mensajes_de_error = {}

        for descriptor in descriptores:
            try:
                _ = descriptor["seleccionado"]
            except (TypeError, KeyError, ValueError) as exc:
                mensajes_de_error["descriptores"] = (
                    MENSAJE_FORMATO_DESCRIPTORES_INVALIDO
                )

        for actividad in actividades_reservadas:
            try:
                _ = actividad["nivel"]
            except (TypeError, KeyError, ValueError) as exc:
                mensajes_de_error["actividades_reservadas"] = (
                    MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO
                )

        for eje in ejes_transversales:
            try:
                _ = eje["nivel"]
            except (TypeError, KeyError, ValueError) as exc:
                mensajes_de_error["ejes_transversales"] = (
                    MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO
                )

        if len(mensajes_de_error.keys()) > 0:
            raise ValidationError(mensajes_de_error)

        # Validar datos:
        if self._validar_resultados_de_aprendizaje(
            resultados_de_aprendizaje=resultados_de_aprendizaje,
        ):
            with transaction.atomic():
                # Modifico el programa. Si falla algo, saltara una excepcion
                resultados = json.loads(resultados_de_aprendizaje)
                version_programa.resultados_de_aprendizaje = resultados
                version_programa.contenidos = contenidos
                version_programa.bibliografia = bibliografia
                version_programa.recursos = recursos
                version_programa.evaluacion = evaluacion
                version_programa.investigacion_docentes = investigacion_docentes
                version_programa.investigacion_estudiantes = investigacion_estudiantes
                version_programa.extension_docentes = extension_docentes
                version_programa.extension_estudiantes = extension_estudiantes
                version_programa.cronograma = cronograma
                version_programa.metodologia_aplicada = metodologia_aplicada
                version_programa.fundamentacion = fundamentacion
                version_programa.full_clean()
                version_programa.save()

                # Obtengo todos los descriptores
                # La lista de descriptores tiene el siguiente formato:
                # {
                #   "id": int
                #   "seleccionado": boolean
                # }
                for descriptor in descriptores:
                    try:
                        try:
                            instancia_descriptor = Descriptor.objects.get(
                                id=descriptor["id"], tipo=TipoDescriptor.DESCRIPTOR
                            )
                        except Descriptor.DoesNotExist as exc:
                            raise ValidationError(
                                {"descriptores": MENSAJE_DESCRIPTOR_INVALIDO}
                            ) from exc

                        descriptor_programa = ProgramaTieneDescriptor.objects.filter(
                            descriptor=instancia_descriptor,
                            version_programa_asignatura=version_programa,
                        )

                        if not descriptor_programa.exists():
                            if descriptor["seleccionado"]:
                                self._asignar_o_modificar_descriptor_prograna(
                                    instancia_descriptor,
                                    version_programa,
                                    NivelDescriptor.BAJO,
                                )

                        else:
                            instancia = descriptor_programa.first()
                            self._asignar_o_modificar_descriptor_prograna(
                                instancia_descriptor,
                                version_programa,
                                (
                                    NivelDescriptor.BAJO
                                    if descriptor["seleccionado"]
                                    else NivelDescriptor.NADA
                                ),
                                instancia,
                            )

                    except (TypeError, KeyError) as exc:
                        raise ValidationError(
                            {"descriptores": MENSAJE_FORMATO_DESCRIPTORES_INVALIDO}
                        ) from exc

                # Obtengo todos los ejes transversales
                # La lista de ejes transversales tiene el siguiente formato:
                # {
                #   "id": int,
                #   "nivel": int
                # }

                for eje in ejes_transversales:
                    try:
                        try:
                            instancia_eje_transversal = Descriptor.objects.get(
                                id=eje["id"]
                            )
                        except Descriptor.DoesNotExist as exc:
                            raise ValidationError(
                                {"ejes_transversales": MENSAJE_EJE_TRANSVERSAL_INVALIDO}
                            ) from exc

                        try:
                            eje_transversal_programa = (
                                ProgramaTieneDescriptor.objects.get(
                                    descriptor=instancia_descriptor,
                                    version_programa_asignatura=version_programa,
                                )
                            )

                            self._asignar_o_modificar_descriptor_prograna(
                                instancia_eje_transversal,
                                version_programa,
                                eje["nivel"],
                                eje_transversal_programa,
                            )
                        except ProgramaTieneDescriptor.DoesNotExist:
                            if eje["nivel"] != NivelDescriptor.NADA:
                                self._asignar_o_modificar_descriptor_prograna(
                                    instancia_eje_transversal,
                                    version_programa,
                                    eje["nivel"],
                                )

                    except (TypeError, KeyError, ValueError) as exc:
                        raise ValidationError(
                            {
                                "ejes_transversales": MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO
                            }
                        ) from exc

                # Obtengo todas las actividades reservadas
                # La lista de actividades reservadas tiene el siguiente formato:
                # {
                #   "id": int,
                #   "nivel": int
                # }

                for actividad in actividades_reservadas:
                    try:
                        try:
                            instancia_actividad_reservada = (
                                ActividadReservada.objects.get(id=actividad["id"])
                            )
                        except ActividadReservada.DoesNotExist as exc:
                            raise ValidationError(
                                {
                                    "actividades_reservadas": MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA
                                }
                            ) from exc

                        try:
                            actividad_reservada_programa = (
                                ProgramaTieneActividadReservada.objects.get(
                                    version_programa_asignatura=version_programa,
                                    actividad_reservada=instancia_actividad_reservada,
                                )
                            )

                            self._asignar_o_modificar_nivel_actividad_reservada(
                                instancia_actividad_reservada,
                                version_programa,
                                actividad["nivel"],
                                actividad_reservada_programa,
                            )
                        except ProgramaTieneActividadReservada.DoesNotExist:
                            if actividad["nivel"] != NivelDescriptor.NADA:
                                self._asignar_o_modificar_nivel_actividad_reservada(
                                    instancia_actividad_reservada,
                                    version_programa,
                                    actividad["nivel"],
                                )
                    except (TypeError, KeyError, ValueError) as exc:
                        raise ValidationError(
                            {
                                "actividades_reservadas": MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO
                            }
                        ) from exc

                # Obtengo todas las correlativas
                # La lista de correlativas tiene el siguiente formato:
                # {
                #   "id": int | None,
                #   "tipo": TipoCorrelativa,
                #   "requisito": RequisitoCorrelativa,
                #   "cantidadAsignaturas": int | None
                #   "asignatura": {
                #     "id": int,
                #     "informacion": str
                #   } | None,
                #   "modulo": str | None
                # }

                try:
                    ids_correlativas_formulario = [
                        correlativa["id"] for correlativa in correlativas
                    ]
                    instancias_correlativa_asignatura = Correlativa.objects.filter(
                        version_programa_asignatura_id=version_programa.id
                    )

                    for instancia_correlativa in instancias_correlativa_asignatura:
                        if instancia_correlativa.id not in ids_correlativas_formulario:
                            instancia_correlativa.delete()

                except Exception:
                    raise ValidationError(
                        {"correlativas": MENSAJE_CORRELATIVA_INVALIDA}
                    )

                for correlativa in correlativas:
                    try:
                        instancia_correlativa = Correlativa.objects.get(
                            id=correlativa["id"]
                        )
                        self._asignar_o_modificar_correlativa(
                            version_programa_asignatura=version_programa,
                            objeto_correlativa=correlativa,
                            instancia_correlativa=instancia_correlativa,
                        )
                    except Correlativa.DoesNotExist:
                        self._asignar_o_modificar_correlativa(
                            version_programa_asignatura=version_programa,
                            objeto_correlativa=correlativa,
                        )
                    except Exception:
                        raise ValidationError(
                            {"correlativas": MENSAJE_CORRELATIVA_INVALIDA}
                        )

            return version_programa

    def presentar_programa_para_aprobacion(self, programa: VersionProgramaAsignatura):
        # TODO. Enviar mail avisando a los directores de carrera
        programa.estado = EstadoAsignatura.PENDIENTE
        programa.save()

        subject = f"[{programa.asignatura.codigo} - {programa.asignatura.denominacion}] Programa listo para corrección."
        context = {
            "site_url": f"{settings.BASE_FRONTEND_URL}/tareas-pendientes",
            "asignatura": programa.asignatura.denominacion,
        }

        # obtener destinatarios
        planes_de_estudio_relacionados = programa.asignatura.planes_de_estudio.all()
        carreras_de_planes_de_estudio = set()

        for plan in planes_de_estudio_relacionados:
            carreras_de_planes_de_estudio.add(plan.carrera)

        directores_de_carrera = set()
        for carrera in carreras_de_planes_de_estudio:
            roles = Rol.objects.filter(
                carrera_id=carrera.id, rol=Roles.DIRECTOR_CARRERA
            )
            for rol in roles:
                directores_de_carrera.add(rol.usuario.email)

        enviar_email_async.delay(
            TiposDeEmail.PROGRAMA_LISTO_PARA_CORRECCION,
            list(directores_de_carrera),
            subject,
            context,
        )
        return programa

    def obtener_ultimo_programa_de_asignatura_aprobado(self, asignatura: Asignatura):
        semestre_dictado_asignatura = asignatura.semestre_dictado
        semestre_actual = self.servicio_semestre.obtener_semestre_actual()

        if semestre_dictado_asignatura is None:
            return VersionProgramaAsignatura.objects.get(
                semestre_id=semestre_actual.id,
                asignatura_id=asignatura.id,
                estado=EstadoAsignatura.APROBADO,
            )

        else:
            semestre_anterior = self.servicio_semestre.obtener_semestre_anterior(
                semestre_dictado_asignatura
            )
            return VersionProgramaAsignatura.objects.get(
                semestre_id=semestre_anterior.id,
                asignatura_id=asignatura.id,
                estado=EstadoAsignatura.APROBADO,
            )

    def reutilizar_ultimo_plan(self, asignatura: Asignatura):
        """
        Toma la ultima version del plan de la asignatura, y crea una nueva con los mismos datos.
        """
        # TODO. Fijarse que no exista ya un programa para la asignatura para ese semestre

        if not self._es_posible_crear_nueva_version_de_programa(
            asignatura.semestre_dictado
        ):
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        semestre_siguiente = self.servicio_semestre.obtener_semestre_siguiente()
        if self._el_programa_ya_existe(
            asignatura=asignatura, semestre=semestre_siguiente
        ):
            raise ValidationError({"__all__": MENSAJE_PROGRAMA_YA_EXISTENTE})

        try:
            ultimo_programa = self.obtener_ultimo_programa_de_asignatura_aprobado(
                asignatura
            )
        except VersionProgramaAsignatura.DoesNotExist as e:
            raise ValidationError(
                {"__all__": MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES}
            ) from e

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
            raise ValidationError({"__all__": MENSAJE_FALLO_REUTILIZACION})

        if not ejes.exists():
            raise ValidationError({"__all__": MENSAJE_FALLO_REUTILIZACION})

        actividades_reservadas = ProgramaTieneActividadReservada.objects.filter(
            version_programa_asignatura=ultimo_programa
        )
        if not actividades_reservadas.exists():
            raise ValidationError({"__all__": MENSAJE_FALLO_REUTILIZACION})

        correlativas_programa = Correlativa.objects.filter(
            version_programa_asignatura_id=ultimo_programa.id
        )

        # Asi si alguna falla, que no se guarde nada. Esta bien?
        with transaction.atomic():
            try:
                if self._validar_resultados_de_aprendizaje(
                    resultados_de_aprendizaje=json.dumps(
                        ultimo_programa.resultados_de_aprendizaje
                    ),
                ):
                    nuevo_programa = VersionProgramaAsignatura.objects.create(
                        asignatura=ultimo_programa.asignatura,
                        semestre=self.servicio_semestre.obtener_semestre_siguiente(),
                        estado=EstadoAsignatura.ABIERTO,
                        contenidos=ultimo_programa.contenidos,
                        bibliografia=ultimo_programa.bibliografia,
                        recursos=ultimo_programa.recursos,
                        evaluacion=ultimo_programa.evaluacion,
                        investigacion_docentes=ultimo_programa.investigacion_docentes,
                        investigacion_estudiantes=ultimo_programa.investigacion_estudiantes,
                        extension_docentes=ultimo_programa.extension_docentes,
                        extension_estudiantes=ultimo_programa.extension_docentes,
                        metodologia_aplicada=ultimo_programa.metodologia_aplicada,
                        fundamentacion=ultimo_programa.fundamentacion,
                        cronograma=ultimo_programa.cronograma,
                        resultados_de_aprendizaje=ultimo_programa.resultados_de_aprendizaje,
                    )

                    for descriptor_del_programa in descriptores_del_programa:
                        self._asignar_o_modificar_descriptor_prograna(
                            descriptor=descriptor_del_programa.descriptor,
                            programa=nuevo_programa,
                            nivel=descriptor_del_programa.nivel,
                        )
                    for actividad_reservada in actividades_reservadas:
                        self._asignar_o_modificar_nivel_actividad_reservada(
                            actividad=actividad_reservada.actividad_reservada,
                            programa=nuevo_programa,
                            nivel=actividad_reservada.nivel,
                        )

                    for correlativa in correlativas_programa:
                        correlativa_nueva = Correlativa(
                            version_programa_asignatura=nuevo_programa,
                            asignatura_correlativa=correlativa.asignatura_correlativa,
                            tipo=correlativa.tipo,
                            requisito=correlativa.requisito,
                            modulo=correlativa.modulo,
                            cantidad_asignaturas=correlativa.cantidad_asignaturas,
                        )
                        correlativa_nueva.full_clean()
                        correlativa_nueva.save()

                    self.presentar_programa_para_aprobacion(nuevo_programa)
                    return nuevo_programa
            except ValidationError as e:
                raise ValidationError({"__all__": MENSAJE_FALLO_REUTILIZACION})

        return None

    def listar_tareas_pendientes_roles(self, roles: QuerySet[Rol]):
        tareas_pendientes = []
        for rol in roles:
            tareas_pendientes += self._listar_tareas_pendientes_para_rol(rol)
        return tareas_pendientes

    def _crear_objeto_para_lista_de_tareas_pendientes(
        self,
        asignatura: Asignatura,
        version_programa: Optional[VersionProgramaAsignatura] = None,
    ) -> dict:
        se_puede_usar_ultimo = version_programa is None
        try:
            if asignatura.semestre_dictado is None:
                semestre_para_reutilizar = (
                    self.servicio_semestre.obtener_semestre_actual()
                )
            else:
                semestre_para_reutilizar = (
                    self.servicio_semestre.obtener_semestre_anterior(
                        asignatura.semestre_dictado
                    )
                )

        except ValidationError:
            semestre_para_reutilizar = None

        if semestre_para_reutilizar is None:
            se_puede_usar_ultimo = False

        if se_puede_usar_ultimo:
            se_puede_usar_ultimo = VersionProgramaAsignatura.objects.filter(
                semestre=semestre_para_reutilizar, asignatura=asignatura
            ).exists()

        revisar = False
        se_puede_modificar = (
            version_programa is not None
            and version_programa.estado == EstadoAsignatura.ABIERTO
        )

        if version_programa is None:
            accion = "Crear nueva versión de Programa de Asignatura."
        elif version_programa.estado == EstadoAsignatura.ABIERTO:
            accion = "Presentar Programa de Asignatura."
        else:
            accion = "Revisar Programa de Asignatura."
            revisar = True

        return {
            "asignatura": SerializerAsignatura(asignatura).data,
            "id_programa": (
                version_programa.id if version_programa is not None else None
            ),
            "accion_requerida": accion,
            "acciones_posibles": {
                "ver_programa": version_programa is not None,
                "modificar_programa": se_puede_modificar,
                "reutilizar_ultimo": se_puede_usar_ultimo,
                "modificar_ultimo": se_puede_usar_ultimo,
                "nuevo": version_programa is None,
                "revisar_programa": revisar,
            },
        }

    def _listar_tareas_pendientes_para_rol(self, rol: Rol) -> list:
        semestre_siguente = self.servicio_semestre.obtener_semestre_siguiente()

        if rol.rol == Roles.DOCENTE or rol.rol == Roles.TITULAR_CATEDRA:
            if not self._es_posible_crear_nueva_version_de_programa(
                rol.asignatura.semestre_dictado
            ):
                return []

            try:
                version = VersionProgramaAsignatura.objects.get(
                    semestre=semestre_siguente,
                    asignatura=rol.asignatura,
                )
            except VersionProgramaAsignatura.DoesNotExist:
                return [
                    self._crear_objeto_para_lista_de_tareas_pendientes(rol.asignatura)
                ]

            if version.estado == EstadoAsignatura.ABIERTO:
                return [
                    self._crear_objeto_para_lista_de_tareas_pendientes(
                        rol.asignatura, version
                    )
                ]

            return []

        if rol.rol == Roles.DIRECTOR_CARRERA:
            # Obtengo todas las materias para la carerra actual. Para eso primero debo obtener los planes.
            planes = self.servicio_planes.obtener_planes_activos_de_carrera(rol.carrera)
            id_planes = [plan.id for plan in planes]
            asignaturas = Asignatura.objects.filter(planes_de_estudio__id__in=id_planes)
            id_asignaturas = [asignatura.id for asignatura in asignaturas]

            versiones = VersionProgramaAsignatura.objects.filter(
                asignatura_id__in=id_asignaturas,
                semestre=semestre_siguente,
                estado=EstadoAsignatura.PENDIENTE,
            )

            tareas_pendientes_director = []
            for version in versiones:
                try:
                    auditoria = AuditoriaEstadoVersionPrograma.objects.get(
                        version_programa_id=version.id, rol_id=rol.id
                    )

                    if auditoria.estado != EstadosAprobacionPrograma.APROBADO:
                        tarea = self._crear_objeto_para_lista_de_tareas_pendientes(
                            version.asignatura, version
                        )
                        tareas_pendientes_director.append(tarea)
                except AuditoriaEstadoVersionPrograma.DoesNotExist:
                    tarea = self._crear_objeto_para_lista_de_tareas_pendientes(
                        version.asignatura, version
                    )
                    tareas_pendientes_director.append(tarea)

            return tareas_pendientes_director

        if rol.rol == Roles.SECRETARIO:
            return []

    def _verificar_programa_queda_aprobado(
        self, version_programa: VersionProgramaAsignatura
    ):
        planes_de_estudio_relacionados = (
            version_programa.asignatura.planes_de_estudio.all()
        )
        carreras_de_planes_de_estudio = set()

        for plan in planes_de_estudio_relacionados:
            carreras_de_planes_de_estudio.add(plan.carrera.id)

        roles = Rol.objects.filter(
            carrera__id__in=carreras_de_planes_de_estudio, rol=Roles.DIRECTOR_CARRERA
        )

        for rol in roles:
            # Se que esto esta horriblemente ineficiente pero son 50 usuarios saludos
            try:
                auditoria = AuditoriaEstadoVersionPrograma.objects.get(
                    version_programa_id=version_programa.id, rol_id=rol.id
                )

                if auditoria.estado != EstadosAprobacionPrograma.APROBADO:
                    return False
            except AuditoriaEstadoVersionPrograma.DoesNotExist:
                return False

        return True

    def _tiene_permiso_para_corregir_programas(
        self, rol: Rol, version_programa: VersionProgramaAsignatura
    ):
        if rol.rol != Roles.DIRECTOR_CARRERA:
            return False

        carrera_rol = rol.carrera
        planes_de_estudio_relacionados = (
            version_programa.asignatura.planes_de_estudio.all()
        )
        carreras_de_planes_de_estudio = set()
        for plan in planes_de_estudio_relacionados:
            carreras_de_planes_de_estudio.add(plan.carrera)

        if not (carrera_rol in carreras_de_planes_de_estudio):
            return False

        return True

    def pedir_cambios_programa_asignatura(
        self, version_programa: VersionProgramaAsignatura, rol: Rol, mensaje: str
    ):
        if not version_programa.estado == EstadoAsignatura.PENDIENTE:
            raise ValidationError({"__all__": MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR})
        if not self._tiene_permiso_para_corregir_programas(rol, version_programa):
            raise ValidationError(
                {"__all__": MENSAJE_PROGRAMA_NO_SE_ENCUENTRA_DISPONIBLE_PARA_CORREGIR}
            )

        try:
            auditoria_anterior = AuditoriaEstadoVersionPrograma.objects.get(
                rol_id=rol.id, version_programa_id=version_programa.id
            )

            auditoria_anterior.estado = EstadosAprobacionPrograma.PEDIDO_CAMBIOS
            auditoria_anterior.mensaje_cambios = mensaje
            auditoria_anterior.full_clean()
            auditoria_anterior.save(update_fields=["estado", "mensaje_cambios"])

        except AuditoriaEstadoVersionPrograma.DoesNotExist:
            nueva_auditoria = AuditoriaEstadoVersionPrograma(
                version_programa=version_programa,
                rol=rol,
                estado=EstadosAprobacionPrograma.PEDIDO_CAMBIOS,
                mensaje_cambios=mensaje,
            )
            nueva_auditoria.full_clean()
            nueva_auditoria.save()

        auditorias = AuditoriaEstadoVersionPrograma.objects.filter(
            version_programa_id=version_programa.id,
            estado=EstadosAprobacionPrograma.APROBADO,
        )
        auditorias.update(
            estado=EstadosAprobacionPrograma.APROBACION_DEPRECADA,
            modificado_en=obtener_fecha_y_hora_actual(),
        )

        version_programa.estado = EstadoAsignatura.ABIERTO
        version_programa.full_clean()
        version_programa.save(update_fields=["estado"])

        docentes_de_la_asignatura = set()
        subject = f"[{version_programa.asignatura.codigo} - {version_programa.asignatura.denominacion}] Se requieren correcciones para el programa."
        context = {
            "site_url": f"{settings.BASE_FRONTEND_URL}/tareas-pendientes",
            "asignatura": version_programa.asignatura.denominacion,
            "mensaje": mensaje,
        }
        roles = Rol.objects.filter(
            Q(rol=Roles.DOCENTE) | Q(rol=Roles.TITULAR_CATEDRA),
            asignatura_id=version_programa.asignatura.id,
        )
        for rol_docente in roles:
            docentes_de_la_asignatura.add(rol_docente.usuario.email)

        enviar_email_async.delay(
            TiposDeEmail.CAMBIOS_PEDIDOS,
            list(docentes_de_la_asignatura),
            subject,
            context,
        )

    def aprobar_programa_de_asignatura(
        self, version_programa: VersionProgramaAsignatura, rol: Rol
    ):
        if not version_programa.estado == EstadoAsignatura.PENDIENTE:
            raise ValidationError({"__all__": MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR})
        if not self._tiene_permiso_para_corregir_programas(rol, version_programa):
            raise ValidationError(
                {"__all__": MENSAJE_PROGRAMA_NO_SE_ENCUENTRA_DISPONIBLE_PARA_CORREGIR}
            )

        try:
            auditoria_anterior = AuditoriaEstadoVersionPrograma.objects.get(
                rol_id=rol.id,
                estado__in=[
                    EstadosAprobacionPrograma.APROBACION_DEPRECADA,
                    EstadosAprobacionPrograma.PEDIDO_CAMBIOS,
                ],
                version_programa_id=version_programa.id,
            )
            auditoria_anterior.estado = EstadosAprobacionPrograma.APROBADO
            auditoria_anterior.modificado_en = obtener_fecha_y_hora_actual()
            auditoria_anterior.full_clean()
            auditoria_anterior.save(update_fields=["estado", "modificado_en"])
        except AuditoriaEstadoVersionPrograma.DoesNotExist:
            nueva_auditoria = AuditoriaEstadoVersionPrograma(
                version_programa=version_programa,
                rol=rol,
                estado=EstadosAprobacionPrograma.APROBADO,
                mensaje_cambios="Aprobado",
            )
            nueva_auditoria.full_clean()
            nueva_auditoria.save()

        if self._verificar_programa_queda_aprobado(version_programa):
            version_programa.estado = EstadoAsignatura.APROBADO
            version_programa.full_clean()
            version_programa.save(update_fields=["estado"])

            docentes_de_la_asignatura = set()
            subject = f"[{version_programa.asignatura.codigo} - {version_programa.asignatura.denominacion}] Programa aprobado."
            roles = Rol.objects.filter(
                Q(rol=Roles.DOCENTE) | Q(rol=Roles.TITULAR_CATEDRA),
                asignatura_id=version_programa.asignatura.id,
            )
            for rol_docente in roles:
                docentes_de_la_asignatura.add(rol_docente.usuario.email)

            enviar_email_async.delay(
                TiposDeEmail.PROGRAMA_APROBADO,
                list(docentes_de_la_asignatura),
                subject,
                {
                    "asignatura": version_programa.asignatura.denominacion,
                },
            )

    def obtener_datos_para_nuevo_programa(self, asignatura: Asignatura):
        # obtengo todos los estandares/programas a los que pertenece la asignatura
        carreras = Carrera.objects.filter(
            plandeestudio__asignaturas=asignatura
        ).distinct()
        carreras_id = [carrera.id for carrera in carreras]
        # obtengo todos los estandares relacionadas a la carrera
        estandares = Estandar.objects.filter(carrera_id__in=carreras_id)
        estandares_id = [estandar.id for estandar in estandares]

        # Obtengo las actividades reservadas
        actividades_reservadas_disponibles_para_nuevo_programa = (
            ActividadReservada.objects.filter(estandar_id__in=estandares_id)
        )

        # obtengo todos los descriptores posibles
        descriptores_del_programa_disponibles_para_nuevo_programa = set()
        ejes_transversales_del_programa_disponibles = set()
        for estandar in estandares:
            for descriptor in estandar.descriptores.filter(
                tipo=TipoDescriptor.DESCRIPTOR
            ):
                descriptores_del_programa_disponibles_para_nuevo_programa.add(
                    descriptor
                )
            for eje in estandar.descriptores.filter(
                tipo=TipoDescriptor.EJE_TRANSVERSAL
            ):
                ejes_transversales_del_programa_disponibles.add(eje)

        ejes_transversales_del_programa = [
            {"id": eje.id, "nombre": eje.descripcion, "nivel": NivelDescriptor.NADA}
            for eje in ejes_transversales_del_programa_disponibles
        ]
        descriptores_del_programa = [
            {
                "id": descriptor.id,
                "nombre": descriptor.descripcion,
                "seleccionado": False,
            }
            for descriptor in descriptores_del_programa_disponibles_para_nuevo_programa
        ]
        actividades_reservadas_del_programa = [
            {
                "id": actividad.id,
                "nombre": actividad.descripcion,
                "nivel": NivelDescriptor.NADA,
            }
            for actividad in actividades_reservadas_disponibles_para_nuevo_programa
        ]

        equipo_docente = Rol.objects.filter(
            rol__in=[Roles.TITULAR_CATEDRA, Roles.DOCENTE], asignatura_id=asignatura.id
        )
        equipo_docente_inforamacion = [
            {
                "id": rol.id,
                "informacion": f"{str(rol.usuario)} - {rol.get_rol()} - {rol.get_dedicacion()}",
            }
            for rol in equipo_docente
        ]

        return {
            "informacion_general": {
                "nombre_asignatura": asignatura.denominacion,
                "codigo_aignatura": asignatura.codigo,
                "anio_academico": "-",
                "bloque_curricular": asignatura.bloque_curricular.nombre,
                "carreras": [
                    {"id": carrera.id, "informacion": carrera.nombre}
                    for carrera in carreras
                ],
                "equipo_docente": equipo_docente_inforamacion,
            },
            "carga_horaria": {
                "semanas_dictado": asignatura.semanas_dictado,
                "teoria_presencial": asignatura.semanal_teoria_presencial,
                "practica_presencial": asignatura.semanal_practica_presencial,
                "teorico_practico_presencial": asignatura.semanal_teorico_practico_presencial,
                "laboratorio_presencial": asignatura.semanal_lab_presencial,
                "teoria_distancia": asignatura.semanal_teoria_remoto,
                "practica_distancia": asignatura.semanal_practica_remoto,
                "teorico_practico_distancia": asignatura.semanal_teorico_practico_remoto,
                "laboratorio_distancia": asignatura.semanal_lab_remoto,
            },
            "ejes_transversales": ejes_transversales_del_programa,
            "descriptores": descriptores_del_programa,
            "actividades_reservadas": actividades_reservadas_del_programa,
        }
