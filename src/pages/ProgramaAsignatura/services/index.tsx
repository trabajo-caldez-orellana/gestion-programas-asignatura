import { client } from '../../../utils/axiosClient'
import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaAPIBody,
  ObtenerProgramaAsignaturaAPIErrorBody,
  NuevoProgramaAPIBody,
  NuevoPrograma
} from '../../../interfaces/interfaces'
import { RUTAS } from '../../../constants/constants'

const parserProgramaAsignatura = (
  programa: ProgramaAsignaturaAPIBody
): ProgramaAsignaturaInterface => {
  return {
    id: programa.id,
    cargaHoraria: {
      practicaDistancia: programa.carga_horaria.practica_distancia,
      teoriaDistancia: programa.carga_horaria.teoria_distancia,
      laboratorioDistancia: programa.carga_horaria.laboratorio_distancia,
      teoricoPracticoDistancia:
        programa.carga_horaria.teorico_practico_distancia,
      practicaPresencial: programa.carga_horaria.practica_presencial,
      teoriaPresencial: programa.carga_horaria.teoria_presencial,
      laboratorioPresencial: programa.carga_horaria.laboratorio_presencial,
      teoricoPracticoPresencial:
        programa.carga_horaria.teorico_practico_presencial,
      semanasDictado: programa.carga_horaria.semanas_dictado
    },
    descriptores: {
      resultadosAprendizaje: programa.descriptores.resultados_de_aprendizaje,
      ejesTransversales: programa.descriptores.ejes_transversales,
      descriptores: programa.descriptores.descriptores,
      actividadesReservadas: programa.descriptores.actividades_reservadas
    },
    informacionAdicional: {
      fundamentacion: programa.informacion_adicional.fundamentacion,
      contenidos: programa.informacion_adicional.contenidos,
      bibliografia: programa.informacion_adicional.bibliografia,
      metodologiaAplicada: programa.informacion_adicional.metodologia_aplicada,
      recursos: programa.informacion_adicional.recursos,
      evaluacion: programa.informacion_adicional.evaluacion,
      investigacionDocentes:
        programa.informacion_adicional.investigacion_docentes,
      investigacionEstudiantes:
        programa.informacion_adicional.investigacion_estudiantes,
      extensionEstudiantes:
        programa.informacion_adicional.extension_estudiantes,
      extensionDocentes: programa.informacion_adicional.extension_docentes
    }
  }
}

const parserNuevoProgramaAsignatura = (
  datos: NuevoProgramaAPIBody
): NuevoPrograma => {
  return {
    ejesTransversales: datos.ejes_transversales,
    actividadesReservadas: datos.actividades_reservadas,
    descriptores: datos.descriptores
  }
}

const parserErrores = (
  error: ObtenerProgramaAsignaturaAPIErrorBody
): string => {
  return error.error
}

interface BodyInterface {
  data: ProgramaAsignaturaAPIBody
}

export const getProgramaAsignatura = async (id: string) => {
  try {
    const response = await client.get<BodyInterface>(
      `${RUTAS.GET_PROGRAMA_ASIGNATURA}${id}/`
    )
    return {
      status: response.status,
      data: parserProgramaAsignatura(response.data.data)
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    return {
      status: err.response.status,
      error: parserErrores(err.response.data)
    }
  }
}

interface ProgramaNuevoBodyInterface {
  data: NuevoProgramaAPIBody
}

export const getInformacionNuevoPrograma = async (id: string) => {
  try {
    const response = await client.get<ProgramaNuevoBodyInterface>(
      `${RUTAS.GET_DATOS_PARA_NUEVO_PROGRAMA}${id}/`
    )
    return {
      status: response.status,
      data: parserNuevoProgramaAsignatura(response.data.data)
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    return {
      status: err.response.status,
      error: parserErrores(err.response.data)
    }
  }
}

export const getInformacionParaModificacion = async (id: string) => {
  try {
    const response = await client.get<BodyInterface>(
      `${RUTAS.GET_PROGRAMA_PARA_MODIFICAR}${id}/`
    )

    return {
      status: response.status,
      data: parserProgramaAsignatura(response.data.data)
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    return {
      status: err.response.status,
      error: parserErrores(err.response.data)
    }
  }
}

// TODO. Esto creo que se va a eliminar proximamente....
export const postProgramaAsignatura = async (
  programaAsignatura: ProgramaAsignaturaInterface | null,
  isDraft: boolean
) => {
  const response = await client.post(
    `${RUTAS.POST_PROGRAMAS_ASIGNATURAS}/${programaAsignatura?.id}`,
    {
      programaAsignatura,
      isDraft
    }
  )

  return response.data
}
