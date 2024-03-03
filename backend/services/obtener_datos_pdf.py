
from backend.models import VersionProgramaAsignatura, Correlativa, Estandar, ProgramaTieneDescriptor
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from backend.common.choices import TipoCorrelativa, NivelDescriptor
from backend.models import VersionProgramaAsignatura, Rol
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
)
from backend.common.choices import TipoDescriptor

class ObtenerDatosPdf:
    def obtener_datos_programa(self, id_programa):
    # Obtenemos todos los datos que necesitamos para generar el PDF
        try:
            programa = VersionProgramaAsignatura.objects.get(id=id_programa)
        except VersionProgramaAsignatura.DoesNotExist:
            return Response(
                {"error": MENSAJE_ID_INEXISTENTE},
                status=HTTP_400_BAD_REQUEST,
            )
        asignatura = programa.asignatura
        docentes = Rol.objects.filter(asignatura=programa.asignatura).select_related(
            "usuario"
        )
        # Obtener todos los Plan de Estudio asociados a la asignatura
        planes_de_estudio = asignatura.plandeestudio_set.all()

        # Obtenemos las carreras
        carreras = []

        for plan_de_estudio in planes_de_estudio:
            carreras.append(plan_de_estudio.carrera)

        # Obtenemos las correlativas
        correlativas_regular = Correlativa.objects.filter(
            asignatura_correlativa=asignatura, tipo=TipoCorrelativa.REGULAR
        )

        asignaturas_correlativas_regular = [
            correlativa.version_programa_asignatura.asignatura
            for correlativa in correlativas_regular
        ]

        correlativas_aprobado = Correlativa.objects.filter(
            asignatura_correlativa=asignatura, tipo=TipoCorrelativa.APROBADO
        )

        asignaturas_correlativas_aprobado = [
            correlativa.version_programa_asignatura.asignatura
            for correlativa in correlativas_aprobado
        ]

        # Obtenemos el año académico
        anio_academico = programa.semestre.anio_academico.fecha_inicio

        # resultados de aprendizaje es un campo tipo JSON, por lo que se debe convertir a un diccionario
        resultados_de_aprendizaje = programa.resultados_de_aprendizaje
        

        # Obtiene ejes transversales

        ids_carreras = [carrera.id for carrera in carreras]

        estandares = Estandar.objects.filter(carrera_id__in=ids_carreras)

        ejes_transversales_del_programa = []

        ejes_transversales_disponibles_para_modificar_programa = set()
        for estandar in estandares:
            for actividad in estandar.descriptores.filter(
                tipo=TipoDescriptor.EJE_TRANSVERSAL
            ):
                ejes_transversales_disponibles_para_modificar_programa.add(actividad)

        for eje in ejes_transversales_disponibles_para_modificar_programa:
            try: 
                eje_del_programa = ProgramaTieneDescriptor.objects.get(
                    version_programa_asignatura_id=programa.id,
                    descriptor_id=eje.id
                )
                ejes_transversales_del_programa.append(
                    {
                        "id": eje_del_programa.descriptor_id,
                        "nombre": eje_del_programa.descriptor.descripcion,
                        "nivel": eje_del_programa.nivel
                    }
                )
            except ProgramaTieneDescriptor.DoesNotExist:
                ejes_transversales_del_programa.append(
                    {
                        "id": eje.id,
                        "nombre": eje.descripcion,
                        "nivel": NivelDescriptor.NADA
                    }
                )
        # Devolver los datos necesarios para generar el PDF

        return {
            "programa": programa,
            "asignatura": asignatura,
            "docentes": docentes,
            "carreras": carreras,
            "correlativas_regular": asignaturas_correlativas_regular,
            "correlativas_aprobado": asignaturas_correlativas_aprobado,
            "anio_academico": anio_academico,
            "resultados_de_aprendizaje": resultados_de_aprendizaje,
            "ejes_transversales": ejes_transversales_del_programa,
            "bloque_curricular": asignatura.bloque_curricular,
        }
