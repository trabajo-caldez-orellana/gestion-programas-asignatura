from django.db.models import Q
from django.core.exceptions import ValidationError

from backend.models import (
  Carrera,
  PlanDeEstudio,
  Descriptor,
  Asignatura,
  VersionProgramaAsignatura,
  ActividadReservada,
  ProgramaTieneActividadReservada,
  ProgramaTieneDescriptor
)
from backend.common.choices import TipoDescriptor, EstadoAsignatura, NivelDescriptor
from backend.services.semestre import ServicioSemestre
from backend.services.estandar import ServicioEstandar
from backend.common.mensajes_de_error import MENSAJE_NO_ESTAN_TODOS_LOS_PROGRAMAS


# TODO. En el frontend dar la opcion de mostrar los planes de estudio activos!!

class ObtenerDatosMatriz:
    servicio_semestre = ServicioSemestre()
    servicio_estandar = ServicioEstandar()

    def obtener_datos_matriz_de_tributacion(self, 
      carrera: Carrera,
      plan_de_estudio: PlanDeEstudio,
    ) -> list[list]:
        """
          Devuelve una matriz con los datos:
          - Primera fila es la cabecera con los nombres de las materias
          - Las siguientes filas representan cada uno a una actividad reservada, descriptor o eje transversal
            y el nivel de incidencia de cada materia sobre ese descriptor!
        """
        # Obtener el semestre actual:
        semestre_actual = self.servicio_semestre.obtener_semestre_actual()

        # Obtengo el estandar actual
        estandar_actual = self.servicio_estandar.obtener_estandar_activo_de_carrera(carrera)

        # Obtengo todos los descriptores del estandar
        descriptores = Descriptor.objects.filter(estandar__in=[estandar_actual.id], tipo=TipoDescriptor.DESCRIPTOR)
        ejes_transversales = Descriptor.objects.filter(estandar__in=[estandar_actual.id], tipo=TipoDescriptor.EJE_TRANSVERSAL)
        actividades_reservadas = ActividadReservada.objects.filter(estandar_id=estandar_actual.id)

        # Obtengo todas las asignaturas del plan actual para el semestre actual!
        semestres_para_filtrar = Q(semestre_dictado__isnull=True) | Q(semestre_dictado = semestre_actual.semestre)
        asignaturas = Asignatura.objects.filter(semestres_para_filtrar, planes_de_estudio__in=[plan_de_estudio.id])

        # Ahora obtengo todos los programas de asignatura de las materias. Tira error 
        # si alguno de los programas no esta completo
        programas_de_asignatura = []
        for asignatura in asignaturas:
          try:
            version = VersionProgramaAsignatura.objects.get(
              asignatura_id=asignatura.id,
              semestre_id=semestre_actual.id,
              estado=EstadoAsignatura.APROBADO
            )
            programas_de_asignatura.append(version)
          except VersionProgramaAsignatura.DoesNotExist:
             raise ValidationError({"__all__": MENSAJE_NO_ESTAN_TODOS_LOS_PROGRAMAS})
          

        filas_matriz = []
        # Voy armando cada fila de datos para armar el csv
        cabecera_csv = ["Descriptores"] + [programa.asignatura.nombre for programa in programas_de_asignatura]
        filas_matriz.append(cabecera_csv)

        for descriptor in descriptores:
           fila = [descriptor.descripcion]
           for programa in programas_de_asignatura:
              try:
                 descriptor_del_programa = ProgramaTieneDescriptor.objects.get(
                    descriptor_id = descriptor.id,
                    version_programa_asignatura_id = programa.id
                 )
                 fila.append(descriptor_del_programa.nivel)
              except ProgramaTieneDescriptor.DoesNotExist:
                 fila.append(NivelDescriptor.NADA)

        separacion_csv = ["Ejes Transversales"] + ['' for _ in range(len(programas_de_asignatura))]
        filas_matriz.append(separacion_csv)

        for eje in ejes_transversales:
           fila = [eje.descripcion]
           for programa in programas_de_asignatura:
              try:
                 eje_del_programa = ProgramaTieneDescriptor.objects.get(
                    descriptor_id=eje.id,
                    version_programa_asignatura_id = programa.id
                 )
                 fila.append(eje_del_programa.nivel)
              except ProgramaTieneDescriptor.DoesNotExist:
                 fila.append(NivelDescriptor.NADA)

        
        separacion_csv[0] = "Actividades Reservadas"
        filas_matriz.append(separacion_csv)

        for actividad in actividades_reservadas:
           fila = [actividad.descripcion]
           for programa in programas_de_asignatura:
              try:
                 actividad_del_programa = ProgramaTieneActividadReservada.objects.get(
                    actividad_del_programa_id = actividad.id, 
                    version_programa_asignatura_id = programa.id
                 )
                 fila.append(actividad_del_programa.nivel)
              except ProgramaTieneActividadReservada.DoesNotExist:
                 fila.append(NivelDescriptor.NADA)

      
        return filas_matriz
