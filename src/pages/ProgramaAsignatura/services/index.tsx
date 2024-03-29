import { client } from '../../../utils/axiosClient'
import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaAPIBody,
  ObtenerProgramaAsignaturaAPIErrorBody,
  NuevoProgramaAPIBody,
  NuevoPrograma,
  ProgramaAsignaturaErrores
} from '../../../interfaces/interfaces'
import { DatoListaInterface, RUTAS } from '../../../constants/constants'

const parserProgramaAsignatura = (
  programa: ProgramaAsignaturaAPIBody
): ProgramaAsignaturaInterface => {
  return {
    id: programa.id,
    informacionGeneral: {
      nombreAsignatura: programa.informacion_general.nombre_asignatura,
      codigoAsignatura: programa.informacion_general.codigo_aignatura,
      bloqueCurricular: programa.informacion_general.bloque_curricular,
      carreras: programa.informacion_general.carreras,
      equipoDocente: programa.informacion_general.equipo_docente,
      anioAcademico: programa.informacion_general.anio_academico
    },
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
      cronograma: programa.informacion_adicional.cronograma,
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
    },
    // TODO. Parse correlativas desde el backend
    correlativas: []
  }
}

const parserNuevoProgramaAsignatura = (
  datos: NuevoProgramaAPIBody
): NuevoPrograma => {
  return {
    informacionGeneral: {
      nombreAsignatura: datos.informacion_general.nombre_asignatura,
      codigoAsignatura: datos.informacion_general.codigo_aignatura,
      bloqueCurricular: datos.informacion_general.bloque_curricular,
      carreras: datos.informacion_general.carreras,
      equipoDocente: datos.informacion_general.equipo_docente,
      anioAcademico: datos.informacion_general.anio_academico
    },
    cargaHoraria: {
      practicaDistancia: datos.carga_horaria.practica_distancia,
      teoriaDistancia: datos.carga_horaria.teoria_distancia,
      laboratorioDistancia: datos.carga_horaria.laboratorio_distancia,
      teoricoPracticoDistancia: datos.carga_horaria.teorico_practico_distancia,
      practicaPresencial: datos.carga_horaria.practica_presencial,
      teoriaPresencial: datos.carga_horaria.teoria_presencial,
      laboratorioPresencial: datos.carga_horaria.laboratorio_presencial,
      teoricoPracticoPresencial:
        datos.carga_horaria.teorico_practico_presencial,
      semanasDictado: datos.carga_horaria.semanas_dictado
    },
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

export const getInformacionModificarAPartirUltimo = async (id: string) => {
  try {
    const response = await client.get<BodyInterface>(
      `${RUTAS.GET_DATOS_PARA_REUTILIZAR_ULTIMO_PROGRAMA}${id}/`
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

interface ProgramaPOSTBodyInterface {
  resultados_de_aprendizaje: string
  contenidos: string
  bibliografia: string
  evaluacion: string
  investigacion_docentes: string
  investigacion_estudiantes: string
  extension_docentes: string
  extension_estudiantes: string
  metodologia_aplicada: string
  fundamentacion: string
  cronograma: string
  recursos: string
  descriptores: { id: number; seleccionado: boolean }[]
  actividades_reservadas: { id: number; nivel: number }[]
  ejes_transversales: { id: number; nivel: number }[]
  presentar_a_aprobacion: boolean
}

interface ProgramaPOSTBodyErrorInterface {
  resultados_de_aprendizaje?: string[]
  contenidos?: string[]
  bibliografia?: string[]
  evaluacion?: string[]
  investigacion_docentes?: string[]
  investigacion_estudiantes?: string[]
  metodologia_aplicada?: string[]
  fundamentacion?: string[]
  extension_docentes?: string[]
  extension_estudiantes?: string[]
  cronograma?: string[]
  recursos?: string[]
  descriptores?: string[]
  actividades_reservadas?: string[]
  ejes_transversales?: string[]
  __all__?: string[]
  mensaje?: string[]
}

const parseProgramaPOSTBody = (
  programa: ProgramaAsignaturaInterface,
  presentar: boolean
): ProgramaPOSTBodyInterface => {
  const parsedDescriptores = programa.descriptores.descriptores.map(
    (descriptor) => {
      return { id: descriptor.id, seleccionado: descriptor.seleccionado }
    }
  )

  const parsedEjesTransversales = programa.descriptores.ejesTransversales.map(
    (eje) => {
      return { id: eje.id, nivel: eje.nivel }
    }
  )

  const parsedActividadesReservadas =
    programa.descriptores.actividadesReservadas.map((actividad) => {
      return { id: actividad.id, nivel: actividad.nivel }
    })

  return {
    resultados_de_aprendizaje: JSON.stringify(
      programa.descriptores.resultadosAprendizaje
    ),
    contenidos: programa.informacionAdicional.contenidos,
    bibliografia: programa.informacionAdicional.bibliografia,
    evaluacion: programa.informacionAdicional.evaluacion,
    investigacion_docentes: programa.informacionAdicional.investigacionDocentes,
    investigacion_estudiantes:
      programa.informacionAdicional.investigacionEstudiantes,
    extension_docentes: programa.informacionAdicional.extensionDocentes,
    extension_estudiantes: programa.informacionAdicional.extensionEstudiantes,
    cronograma: programa.informacionAdicional.cronograma,
    recursos: programa.informacionAdicional.recursos,
    descriptores: parsedDescriptores,
    actividades_reservadas: parsedActividadesReservadas,
    ejes_transversales: parsedEjesTransversales,
    presentar_a_aprobacion: presentar,
    metodologia_aplicada: programa.informacionAdicional.metodologiaAplicada,
    fundamentacion: programa.informacionAdicional.fundamentacion
  }
}

const parseProgramaPOSTError = (
  responseError: ProgramaPOSTBodyErrorInterface
): ProgramaAsignaturaErrores => {
  return {
    descriptores: {
      resultadosAprendizaje: responseError.resultados_de_aprendizaje
        ? responseError.resultados_de_aprendizaje[0]
        : '',
      ejesTransversales: responseError.ejes_transversales
        ? responseError.ejes_transversales[0]
        : '',
      descriptores: responseError.descriptores
        ? responseError.descriptores[0]
        : '',
      actividadesReservadas: responseError.actividades_reservadas
        ? responseError.actividades_reservadas[0]
        : ''
    },
    informacionAdicional: {
      fundamentacion: responseError.fundamentacion
        ? responseError.fundamentacion[0]
        : '',
      cronograma: responseError.cronograma ? responseError.cronograma[0] : '',
      contenidos: responseError.contenidos ? responseError.contenidos[0] : '',
      bibliografia: responseError.bibliografia
        ? responseError.bibliografia[0]
        : '',
      recursos: responseError.recursos ? responseError.recursos[0] : '',
      evaluacion: responseError.evaluacion ? responseError.evaluacion[0] : '',
      metodologiaAplicada: responseError.metodologia_aplicada
        ? responseError.metodologia_aplicada[0]
        : '',
      investigacionDocentes: responseError.investigacion_docentes
        ? responseError.investigacion_docentes[0]
        : '',
      investigacionEstudiantes: responseError.investigacion_estudiantes
        ? responseError.investigacion_estudiantes[0]
        : '',
      extensionEstudiantes: responseError.extension_estudiantes
        ? responseError.extension_estudiantes[0]
        : '',
      extensionDocentes: responseError.extension_docentes
        ? responseError.extension_docentes[0]
        : ''
    },
    // TODO. Cambiar cuadno cree la llamada a a la api
    correlativas: '',
    all: responseError.__all__ ? responseError.__all__[0] : '',
    mensaje: responseError.mensaje ? responseError.mensaje[0] : ''
  }
}

export const crearProgramaAsignatura = async (
  datos: ProgramaAsignaturaInterface,
  presentar: boolean,
  id_asignatura: number
) => {
  const cuerpoPost = parseProgramaPOSTBody(datos, presentar)

  try {
    const response = await client.post(
      `${RUTAS.POST_CREAR_PROGRAMA_ASIGNATURA}${id_asignatura}/`,
      cuerpoPost
    )

    return {
      status: response.status
    }
  } catch (error: any) {
    return {
      status: error.response.status,
      error: parseProgramaPOSTError(error.response.data.error)
    }
  }
}

export const modificarProgramaAsignatura = async (
  datos: ProgramaAsignaturaInterface,
  presentar: boolean,
  id_programa: number
) => {
  const cuerpoPost = parseProgramaPOSTBody(datos, presentar)

  try {
    const response = await client.post(
      `${RUTAS.POST_EDITAR_PROGRAMA_ASIGNATURA}${id_programa}/`,
      cuerpoPost
    )

    return {
      status: response.status
    }
  } catch (error: any) {
    return {
      status: error.response.status,
      error: parseProgramaPOSTError(error.response.data.error)
    }
  }
}

export const aprobarProgramaAsignatura = async (id_programa: number) => {
  try {
    const response = await client.get(
      `${RUTAS.APROBAR_PROGRAMA}${id_programa}/`
    )

    return {
      status: response.status
    }
  } catch (error: any) {
    return {
      status: error.response.status,
      error: parseProgramaPOSTError(error.response.data.error)
    }
  }
}

export const pedirCambiosProgramaAsignatura = async (
  id_programa: number,
  mensaje: string
) => {
  const cuerpoPost = { mensaje: mensaje }

  try {
    const response = await client.post(
      `${RUTAS.PEDIR_CAMBIOS_PROGRAMA}${id_programa}/`,
      cuerpoPost
    )

    return {
      status: response.status
    }
  } catch (error: any) {
    return {
      status: error.response.status,
      error: parseProgramaPOSTError(error.response.data.error)
    }
  }
}

export const obtenerAsignaturasDisponiblesAPartirDeAsignatura = async (
  id_asignatura: string
) => {
  try {
    const response = await client.post(
      `${RUTAS.OBTENER_CORRELATIVAS_DISPONIBLES_ASIGNATURA}${id_asignatura}/`
    )

    return {
      status: response.status,
      data: response.data.data as DatoListaInterface[]
    }
  } catch (error: any) {
    return {
      status: error.response.status,
      data: [] as DatoListaInterface[]
    }
  }
}

export const obtenerAsignaturasDisponiblesAPartirDePrograma = async (
  id_programa: string
) => {
  try {
    const response = await client.post(
      `${RUTAS.OBTENER_CORRELATIVAS_DISPONIBLES_PROGRAMA}${id_programa}/`
    )

    return {
      status: response.status,
      data: response.data.data as DatoListaInterface[]
    }
  } catch (error: any) {
    return {
      status: error.response.status,
      data: [] as DatoListaInterface[]
    }
  }
}
