export interface CargaHoraria {
  cargaHorariaTotal: number
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
    nombre: string
    valor: number
  }[]
  descriptores: {
    si: { id: number; nombre: string }[]
    no: { id: number; nombre: string }[]
  }
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
  cargaHoraria: CargaHoraria
  descriptores: Descriptor
  informacionAdicional: InformacionAdicional
}
