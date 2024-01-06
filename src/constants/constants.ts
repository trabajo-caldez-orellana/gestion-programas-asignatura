export const RUTAS = {
  GET_PROGRAMA_ASIGNATURA: '/programa-asignaturas',
  POST_PROGRAMAS_ASIGNATURAS: '/programa-asignatura',
  GET_PROGRAMAS_ASIGNATURAS: '/programas-asignaturas/',
  GET_TAREAS_PENDIENTES: '/api/programas/pendientes/'
}
export const HANDLERS = {
  GET_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignaturas/:id',
  POST_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignatura/:id',
  GET_PROGRAMAS_ASIGNATURAS_HANDLER: '/programas-asignaturas/'
}

export const MODOS_PROGRAMA_ASIGNATURA = {
  VER: 'VER',
  NUEVO: 'NUEVO',
  EDITAR: 'EDITAR'
}

// TODO. Esto se usa?
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

type CampoCargaHorariaType = {
  label: string
  id: string
  name: string
}[]

export const CAMPOS_CARGA_HORARIA: CampoCargaHorariaType = [
  {
    label: 'Semanas de dictado',
    id: 'semanas-dictado',
    name: 'semanas_dictado'
  },
  {
    label: 'Teoria presencial',
    id: 'teoria-presencial',
    name: 'teoria_presencial'
  },
  {
    label: 'Practica presencial',
    id: 'practica-presencial',
    name: 'practica_presencial'
  },
  {
    label: 'Teorico-practico presencial',
    id: 'teorico-practico-presencial',
    name: 'teorico_practico_presencial'
  },
  {
    label: 'Laboratorios presenciales',
    id: 'laboratorios-presenciales',
    name: 'laboratorios_presenciales'
  },
  {
    label: 'Teoria a distancia',
    id: 'teoria-distancia',
    name: 'teoria_distancia'
  },
  {
    label: 'Practica a distancia',
    id: 'practica-distancia',
    name: 'practica_distancia'
  },
  {
    label: 'Teorico-practico a distancia',
    id: 'teorico-practico-distancia',
    name: 'teorico_practico_distancia'
  },
  {
    label: 'Laboratorio a distancia',
    id: 'laboratorio-distancia',
    name: 'laboratorio_distancia'
  }
]

type CampoInformacionAdicionalType = {
  label: string
  id: string
  name: string
}[]

export const CAMPOS_INFORMACION_ADICIONAL: CampoInformacionAdicionalType = [
  {
    label: 'Fundamentacion',
    id: 'fundamentacion',
    name: 'fundamentacion'
  },
  {
    label: 'Contenidos',
    id: 'contenidos',
    name: 'contenidos'
  },
  {
    label: 'Bibliografía',
    id: 'bibliografia',
    name: 'bibliografia'
  },
  {
    label: 'Metodología aplicada',
    id: 'metodologia-aplicada',
    name: 'metodologia_aplicada'
  },
  {
    label: 'Recursos',
    id: 'recursos',
    name: 'recursos'
  },
  {
    label: 'Evaluación',
    id: 'evaluacion',
    name: 'evaluacion'
  },
  {
    label: 'Investigación',
    id: 'investigacion',
    name: 'investigacion'
  },
  {
    label: 'Extensión',
    id: 'extension',
    name: 'extension'
  }
]
