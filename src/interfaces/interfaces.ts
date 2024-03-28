import { DatoListaInterface } from '../constants/constants'

export interface CargaHoraria {
  // cargaHorariaTotal: number
  semanasDictado: number
  teoriaPresencial: number
  practicaPresencial: number
  teoricoPracticoPresencial: number
  laboratorioPresencial: number
  teoriaDistancia: number
  practicaDistancia: number
  teoricoPracticoDistancia: number
  laboratorioDistancia: number
  // Index signature
  [key: string]: string | number
}

export interface Descriptor {
  resultadosAprendizaje: string[]
  ejesTransversales: {
    id: number
    nombre: string
    nivel: number
  }[]
  descriptores: {
    id: number
    nombre: string
    seleccionado: boolean
  }[]
  actividadesReservadas: {
    id: number
    nombre: string
    nivel: number
  }[]
}

export interface InformacionAdicional {
  fundamentacion: string
  contenidos: string
  bibliografia: string
  metodologiaAplicada: string
  recursos: string
  evaluacion: string
  investigacionDocentes: string
  investigacionEstudiantes: string
  extensionDocentes: string
  extensionEstudiantes: string
  cronograma: string
  // Index signature
  [key: string]: string
}

export interface InformacionGeneral {
  nombreAsignatura: string
  codigoAsignatura: string
  anioAcademico: string
  bloqueCurricular: string
  carreras: DatoListaInterface[]
  equipoDocente: DatoListaInterface[]
}

export interface ProgramaAsignaturaInterface {
  id: number
  informacionGeneral: InformacionGeneral
  cargaHoraria: CargaHoraria
  descriptores: Descriptor
  informacionAdicional: InformacionAdicional
}

export interface PlanesDeEstudioAPIBody {
  id: number
  nombre: string
  carrera_id: number
  nombre_carrera: string
}

export interface PlanesDeEstudioInterface {
  id: number
  nombre: string
  carreraId: number
  carreraNombre: string
}

export interface MatrizAPIErrorInterface {
  __all__?: string[]
  plan_de_estudio?: string[]
  carrera?: string[]
}

export interface MatrizErroresInterface {
  all: string
  planDeEstudio: string
  carrera: string
}

export interface CargaHorariaErrores {
  semanasDictado: string
  teoriaPresencial: string
  practicaPresencial: string
  teoricoPracticoPresencial: string
  laboratorioPresencial: string
  teoriaDistancia: string
  practicaDistancia: string
  teoricoPracticoDistancia: string
  laboratorioDistancia: string
  // Index signature
  [key: string]: string
}

export interface DescriptorErrores {
  resultadosAprendizaje: string
  ejesTransversales: string
  descriptores: string
  actividadesReservadas: string
}

export interface InformacionAdicionalErrores {
  fundamentacion: string
  contenidos: string
  bibliografia: string
  metodologiaAplicada: string
  recursos: string
  evaluacion: string
  investigacionDocentes: string
  investigacionEstudiantes: string
  extensionDocentes: string
  extensionEstudiantes: string
  cronograma: string
  // Index signature
  [key: string]: string
}

export interface ProgramaAsignaturaErrores {
  descriptores: DescriptorErrores
  informacionAdicional: InformacionAdicionalErrores
  all: string
  mensaje: string
}

export interface NuevoPrograma {
  informacionGeneral: InformacionGeneral
  cargaHoraria: CargaHoraria
  ejesTransversales: {
    id: number
    nombre: string
    nivel: number
  }[]
  descriptores: {
    id: number
    nombre: string
    seleccionado: boolean
  }[]
  actividadesReservadas: {
    id: number
    nombre: string
    nivel: number
  }[]
}

export interface ProgramaAsignaturaAPIBody {
  id: number
  informacion_general: {
    nombre_asignatura: string
    codigo_aignatura: string
    anio_academico: string
    bloque_curricular: string
    carreras: DatoListaInterface[]
    equipo_docente: DatoListaInterface[]
  }
  carga_horaria: {
    semanas_dictado: number
    teoria_presencial: number
    practica_presencial: number
    teorico_practico_presencial: number
    laboratorio_presencial: number
    teoria_distancia: number
    practica_distancia: number
    teorico_practico_distancia: number
    laboratorio_distancia: number
  }
  descriptores: {
    resultados_de_aprendizaje: string[]
    ejes_transversales: {
      id: number
      nombre: string
      nivel: number
    }[]
    descriptores: {
      id: number
      nombre: string
      seleccionado: boolean
    }[]
    actividades_reservadas: {
      id: number
      nombre: string
      nivel: number
    }[]
  }
  informacion_adicional: {
    fundamentacion: string
    cronograma: string
    contenidos: string
    bibliografia: string
    metodologia_aplicada: string
    recursos: string
    evaluacion: string
    investigacion_docentes: string
    investigacion_estudiantes: string
    extension_docentes: string
    extension_estudiantes: string
  }
}

export interface NuevoProgramaAPIBody {
  informacion_general: {
    nombre_asignatura: string
    codigo_aignatura: string
    anio_academico: string
    bloque_curricular: string
    carreras: DatoListaInterface[]
    equipo_docente: DatoListaInterface[]
  }
  carga_horaria: {
    semanas_dictado: number
    teoria_presencial: number
    practica_presencial: number
    teorico_practico_presencial: number
    laboratorio_presencial: number
    teoria_distancia: number
    practica_distancia: number
    teorico_practico_distancia: number
    laboratorio_distancia: number
  }
  ejes_transversales: {
    id: number
    nombre: string
    nivel: number
  }[]
  descriptores: {
    id: number
    nombre: string
    seleccionado: boolean
  }[]
  actividades_reservadas: {
    id: number
    nombre: string
    nivel: number
  }[]
}

export interface ObtenerProgramaAsignaturaAPIErrorBody {
  error: string
}

export interface DatosAsignaturaTareaPendiente {
  id: number
  nombre: string
}

export interface AccionesPosiblesInterface {
  verPrograma: boolean
  modificarPrograma: boolean
  reutilizarUltimo: boolean
  modificarUltimo: boolean
  nuevo: boolean
  revisarPrograma: boolean
}

export interface TareaPendiente {
  asignatura: DatosAsignaturaTareaPendiente
  idPrograma: number | null
  accionRequerida: string
  accionesPosibles: AccionesPosiblesInterface
}
