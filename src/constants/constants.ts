export const RUTAS = {
  GET_PROGRAMA_ASIGNATURA: '/programa-asignaturas',
  POST_PROGRAMAS_ASIGNATURAS: '/programa-asignatura',
  GET_PROGRAMAS_ASIGNATURAS: '/programas-asignaturas/'
}
export const HANDLERS = {
  GET_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignaturas/:id',
  POST_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignatura/:id',
  GET_PROGRAMAS_ASIGNATURAS_HANDLER: '/programas-asignaturas/'
}

export const MODOS_PROGRAMA_ASIGNATURA = {
  VER: 'VER',
  NUEVO: 'NUEVO'
}

export const NUEVO_PROGRAMA_ASIGNATURA = {
  id: 1,
  cargaHoraria: {
    semanasDictado: 0,
    teoriaPresencial: 0,
    practicaPresencial: 0,
    teoricoPracticoPresencial: 0,
    laboratoriosPresenciales: 0,
    teoriaDistancia: 0,
    practicaDistancia: 0,
    teoricoPracticoDistancia: 0,
    laboratorioDistancia: 0
  },
  descriptores: {
    resultadosAprendizaje: [''],
    ejesTransversales: [
      { id: 1, nombre: 'Eje 1', nivel: 0 },
      { id: 2, nombre: 'Eje 2', nivel: 2 }
    ],
    descriptores: [],
    actividadesReservadas: []
  },
  informacionAdicional: {
    fundamentacion: '',
    contenidos: '',
    bibliografia: '',
    metodologiaAplicada: '',
    recursos: '',
    evaluacion: '',
    investigacion: '',
    extension: ''
  }
}
