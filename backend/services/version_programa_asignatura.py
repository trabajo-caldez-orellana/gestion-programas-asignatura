import json
from typing import Optional, List

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

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
    Semestre
)
from backend.common.choices import (
    NivelDescriptor,
    TipoDescriptor,
    EstadoAsignatura,
    Roles,
    Semestres,
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
    MENSAJE_VERSION_ANTERIOR_NO_APROBADA,
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
    MENSAJE_PROGRAMA_YA_EXISTENTE
    
)
from backend.services.semestre import ServicioSemestre
from backend.services.configuracion import ServicioConfiguracion
from backend.services.plan_de_estudio import ServicioPlanDeEstudio
from backend.serializers import SerializerAsignatura


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
        try:
            resultados = json.loads(resultados_de_aprendizaje)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValidationError(
                {"resultados_de_aprendizaje": MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO}
            ) from exc

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

    def _el_programa_ya_existe(self, asignatura: Asignatura, semestre: Semestre) -> bool:
        programas_count = VersionProgramaAsignatura.objects.filter(asignatura_id=asignatura.id, semestre_id=semestre.id).count()
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
    ):
        """
        Crea una nueva version de un programa de asignatura para el semestre que viene!
        """
        # TODO. Fijarse que no exista ya un programa para la asignatura para ese semestre
        print(resultados_de_aprendizaje)
        breakpoint()
        if not self._es_posible_crear_nueva_version_de_programa(
            asignatura.semestre_dictado
        ):
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})

        semestre = self.servicio_semestre.obtener_semestre_siguiente()

        if self._el_programa_ya_existe(asignatura, semestre):
            raise ValidationError({"__all__": MENSAJE_PROGRAMA_YA_EXISTENTE})


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
                version_programa = VersionProgramaAsignatura(
                    estado=EstadoAsignatura.ABIERTO,
                    asignatura=asignatura,
                    semestre=semestre,
                    resultados_de_aprendizaje=resultados_de_aprendizaje,
                    contenidos=contenidos,
                    bibliografia=bibliografia,
                    recursos=recursos,
                    evaluacion=evaluacion,
                    investigacion_docentes=investigacion_docentes,
                    investigacion_estudiantes=investigacion_estudiantes,
                    extension_docentes=extension_docentes,
                    extension_estudiantes=extension_estudiantes,
                    metodologia_aplicada = metodologia_aplicada,
                    fundamentacion = fundamentacion,
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

        cantidad_descriptores = 0
        for descriptor in descriptores:
            try:
                if descriptor["seleccionado"]:
                    cantidad_descriptores += 1
            except (TypeError, KeyError, ValueError) as exc:
                raise ValidationError(
                    {"descriptores": MENSAJE_FORMATO_DESCRIPTORES_INVALIDO}
                ) from exc

        if cantidad_descriptores == 0:
            mensajes_de_error["descriptores"] = MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR

        cantidad_actividades_reservadas = 0
        for actividad in actividades_reservadas:
            try:
                if actividad["nivel"] != NivelDescriptor.NADA:
                    cantidad_actividades_reservadas += 1
            except (TypeError, KeyError, ValueError) as exc:
                raise ValidationError(
                    {
                        "actividades_reservadas": MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO
                    }
                ) from exc

        if cantidad_actividades_reservadas == 0:
            mensajes_de_error[
                "actividades_reservadas"
            ] = MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA

        cantidad_ejes_transversales = 0
        for eje in ejes_transversales:
            try:
                if eje["nivel"] != NivelDescriptor.NADA:
                    cantidad_ejes_transversales += 1
            except (TypeError, KeyError, ValueError) as exc:
                raise ValidationError(
                    {"ejes_transversales": MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO}
                ) from exc

        if cantidad_ejes_transversales == 0:
            mensajes_de_error[
                "ejes_transversales"
            ] = MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL

        if len(mensajes_de_error.keys()) > 0:
            raise ValidationError(mensajes_de_error)

        # Validar datos:
        if self._validar_resultados_de_aprendizaje(
            resultados_de_aprendizaje=resultados_de_aprendizaje,
        ):
            with transaction.atomic():
                # Modifico el programa. Si falla algo, saltara una excepcion

                version_programa.resultados_de_aprendizaje = resultados_de_aprendizaje
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
                                NivelDescriptor.BAJO if descriptor["seleccionado"] else NivelDescriptor.NADA,
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

            return version_programa

    def presentar_programa_para_aprobacion(self, programa: VersionProgramaAsignatura):
        programa.estado = EstadoAsignatura.PENDIENTE
        programa.save()
        return programa

    def obtener_ultimo_programa_de_asignatura_aprobado(self, asignatura: Asignatura):
        semestre_dictado_asignatura = asignatura.semestre_dictado
        semestre_actual = self.servicio_semestre.obtener_semestre_actual()

        if semestre_dictado_asignatura is None:
            return VersionProgramaAsignatura.objects.get(semestre_id = semestre_actual.id, asignatura_id=asignatura.id, estado=EstadoAsignatura.APROBADO)
        
        else:
            semestre_anterior = self.servicio_semestre.obtener_semestre_anterior(semestre_dictado_asignatura)
            return VersionProgramaAsignatura.objects.get(semestre_id = semestre_anterior.id, asignatura_id=asignatura.id, estado=EstadoAsignatura.APROBADO)


    def reutilizar_ultimo_plan(self, asignatura: Asignatura):
        """
        Toma la ultima version del plan de la asignatura, y crea una nueva con los mismos datos.
        """
        # TODO. Fijarse que no exista ya un programa para la asignatura para ese semestre

        if not self._es_posible_crear_nueva_version_de_programa(
            asignatura.semestre_dictado
        ):
            raise ValidationError({"__all__": MENSAJE_PROGRAMAS_CERRADOS})


        if not self._el_programa_ya_existe():
            raise ValidationError({"__all__": MENSAJE_PROGRAMA_YA_EXISTENTE})

        try:
            ultimo_programa = self.obtener_ultimo_programa_de_asignatura_aprobado(asignatura)
        except VersionProgramaAsignatura.DoesNotExist as e:
            raise ValidationError(
                {"asignatura": MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES}
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
            if self._validar_resultados_de_aprendizaje(
                resultados_de_aprendizaje=ultimo_programa.resultados_de_aprendizaje,
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
                    metodologia_aplicada = ultimo_programa.metodologia_aplicada,
                    fundamentacion = ultimo_programa.fundamentacion,
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

                return nuevo_programa

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

            if se_puede_usar_ultimo:
                se_puede_usar_ultimo = VersionProgramaAsignatura.objects.filter(
                    semestre=semestre_para_reutilizar, asignatura=asignatura
                ).exists()
        except ValidationError as e:
            pass

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

        return {
            "asignatura": SerializerAsignatura(asignatura).data,
            "id_programa": version_programa.id
            if version_programa is not None
            else None,
            "accion_requerida": accion,
            "acciones_posibles": {
                "ver_programa": version_programa is not None,
                "modificar_programa": se_puede_modificar,
                "reutilizar_ultimo": se_puede_usar_ultimo,
                "modificar_ultimo": se_puede_usar_ultimo,
                "nuevo": version_programa is None,
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
                    estado__in=[EstadoAsignatura.ABIERTO, EstadoAsignatura.PENDIENTE]
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
            asignaturas = Asignatura.objects.filter(plandeestudio__id__in=id_planes)
            id_asignaturas = [asignatura.id for asignatura in asignaturas]

            versiones = VersionProgramaAsignatura.objects.filter(
                asignatura_id__in=id_asignaturas,
                semestre=semestre_siguente,
                estado=EstadoAsignatura.PENDIENTE,
            )

            return [
                self._crear_objeto_para_lista_de_tareas_pendientes(
                    version.asignatura, version
                )
                for version in versiones
            ]

        if rol.rol == Roles.SECRETARIO:
            return []

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
                descriptores_del_programa_disponibles_para_nuevo_programa.add(descriptor)
            for eje in estandar.descriptores.filter(
                tipo=TipoDescriptor.EJE_TRANSVERSAL
            ):
                ejes_transversales_del_programa_disponibles.add(eje)


        ejes_transversales_del_programa = [
            {"id": eje.id, "nombre": eje.descripcion, "nivel": NivelDescriptor.NADA}
            for eje in ejes_transversales_del_programa_disponibles
        ]
        descriptores_del_programa = [
            {"id": descriptor.id, "nombre": descriptor.descripcion, "seleccionado": False}
            for descriptor in descriptores_del_programa_disponibles_para_nuevo_programa
        ]
        actividades_reservadas_del_programa = [
            {"id": actividad.id, "nombre": actividad.descripcion, "nivel": NivelDescriptor.NADA}
            for actividad in actividades_reservadas_disponibles_para_nuevo_programa
        ]

        return {
            "ejes_transversales": ejes_transversales_del_programa,
            "descriptores": descriptores_del_programa,
            "actividades_reservadas": actividades_reservadas_del_programa
        }