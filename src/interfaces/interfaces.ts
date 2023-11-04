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
}

export interface ProgramaAsignatura {
  id: number
  cargaHoraria: CargaHoraria
  descriptores: Descriptor
  informacionAdicional: InformacionAdicional
}
