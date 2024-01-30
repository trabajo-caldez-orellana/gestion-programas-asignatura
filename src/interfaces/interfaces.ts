export interface CargaHoraria {
  // cargaHorariaTotal: number
  semanasDictado: number
  teoriaPresencial: number
  practicaPresencial: number
  teoricoPracticoPresencial: number
  laboratoriosPresenciales: number
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
  actividadesReservadas: string[]
}

export interface InformacionAdicional {
  fundamentacion: string
  contenidos: string
  bibliografia: string
  metodologiaAplicada: string
  recursos: string
  evaluacion: string
  investigacion: string
  extension: string
  // Index signature
  [key: string]: string | number
}

export interface ProgramaAsignatura {
  id: number
  cargaHoraria: CargaHoraria
  descriptores: Descriptor
  informacionAdicional: InformacionAdicional
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
}

export interface TareaPendiente {
  asignatura: DatosAsignaturaTareaPendiente
  idPrograma: number | null
  accionRequerida: string
  accionesPosibles: AccionesPosiblesInterface
}
