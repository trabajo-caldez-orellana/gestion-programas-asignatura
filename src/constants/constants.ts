import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores
} from 'interfaces/interfaces'

import {
  Inicio,
  Carrera,
  PlanEstudio,
  Descriptores,
  BloqueCurricular,
  Historial,
  ProgramaAsignatura,
  TareasPendientes,
  ProgramasVigentes,
  Auditoria
} from '../pages'

export const RUTAS = {
  GET_PROGRAMA_ASIGNATURA: '/api/programas/',
  GET_PROGRAMAS_ASIGNATURAS: '/api/programas/',
  GET_PROGRAMAS_VIGENTES: '/api/programas/vigentes/',
  GET_PROGRAMA_PARA_MODIFICAR: '/api/informacion-formularios/editar/',
  GET_DATOS_PARA_NUEVO_PROGRAMA: '/api/informacion-formularios/nuevo/',
  GET_DATOS_PARA_REUTILIZAR_ULTIMO_PROGRAMA:
    '/api/informacion-formularios/editar_ultimo/',
  GET_TAREAS_PENDIENTES: '/api/programas/pendientes/',
  GET_FILTROS_HISTORIAL: 'api/filtros/',
  GET_HISTORIAL: 'api/historial/',
  POST_CREAR_PROGRAMA_ASIGNATURA: 'api/programas/nuevo/',
  POST_EDITAR_PROGRAMA_ASIGNATURA: 'api/programas/editar/'
}

export const HANDLERS = {
  GET_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignaturas/:id',
  POST_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignatura/:id',
  GET_PROGRAMAS_ASIGNATURAS_HANDLER: '/programas-asignaturas/',
  GET_PROGRAMAS_VIGENTES_HANDLER: '/api/programas/vigentes/',
  GET_FILTROS_HISTORIAL_HANDLER: 'api/filtros/',
  GET_HISTORIAL: 'api/historial/'
}

export const MODOS_PROGRAMA_ASIGNATURA = {
  VER: 'ver',
  NUEVO: 'nuevo',
  EDITAR: 'editar',
  EDITAR_ULTIMO: 'editar-ultimo'
}

export const NUEVO_PROGRAMA_ASIGNATURA: ProgramaAsignaturaInterface = {
  id: 1,
  cargaHoraria: {
    semanasDictado: 0,
    teoriaPresencial: 0,
    practicaPresencial: 0,
    teoricoPracticoPresencial: 0,
    laboratorioPresencial: 0,
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
    cronograma: '',
    contenidos: '',
    bibliografia: '',
    metodologiaAplicada: '',
    recursos: '',
    evaluacion: '',
    investigacionDocentes: '',
    investigacionEstudiantes: '',
    extensionEstudiantes: '',
    extensionDocentes: ''
  }
}

export const ERRORES_DEFAULT_PROGRAMA_ASIGNATURA: ProgramaAsignaturaErrores = {
  descriptores: {
    resultadosAprendizaje: '',
    ejesTransversales: '',
    descriptores: '',
    actividadesReservadas: ''
  },
  informacionAdicional: {
    fundamentacion: '',
    cronograma: '',
    contenidos: '',
    bibliografia: '',
    metodologiaAplicada: '',
    recursos: '',
    evaluacion: '',
    investigacionDocentes: '',
    investigacionEstudiantes: '',
    extensionEstudiantes: '',
    extensionDocentes: ''
  },
  all: ''
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
    label: 'Cronograma',
    id: 'cronograma',
    name: 'cronograma'
  },
  {
    label: 'Bibliografía',
    id: 'bibliografia',
    name: 'bibliografia'
  },
  {
    label: 'Metodología aplicada',
    id: 'metodologiaAplicada',
    name: 'metodologiaAplicada'
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
    label: 'Investigación Estudiantes',
    id: 'investigacionEstudiantes',
    name: 'investigacionEstudiantes'
  },
  {
    label: 'Investigación Docentes',
    id: 'investigacionDocentes',
    name: 'investigacionDocentes'
  },
  {
    label: 'Extensión Estudiantes',
    id: 'extensionEstudiantes',
    name: 'extensionEstudiantes'
  },
  {
    label: 'Extensión Docentes',
    id: 'extensionDocentes',
    name: 'extensionDocentes'
  }
]

type SidebarSection = {
  id: number
  name: string
  sections: {
    id: number
    name: string
    url: string
  }[]
}

export const RUTAS_PAGINAS = {
  INICIO: '',
  CARRERA: '/carrera',
  PLAN_DE_ESTUDIO: '/plan-estudio',
  DESCRIPTORES: '/descriptores',
  BLOQUE_CURRICULAR: '/bloque-curricular',
  PROGRAMA_DE_ASIGNATURA: '/programa-asignatura',
  AUDITORIA: '/auditoria',
  PROGRAMAS_VIGENTES: '/programas-vigentes',
  TAREAS_PENDIENTES: '/tareas-pendientes',
  HISTORIAL: '/historial'
}

export const SIDEBAR_SECTIONS: SidebarSection[] = [
  {
    id: 1,
    name: 'Carrera',
    sections: [
      {
        id: 1,
        name: 'Carrera',
        url: RUTAS_PAGINAS.CARRERA
      },
      {
        id: 2,
        name: 'Plan de Estudio',
        url: RUTAS_PAGINAS.PLAN_DE_ESTUDIO
      },
      {
        id: 3,
        name: 'Descriptores',
        url: RUTAS_PAGINAS.DESCRIPTORES
      }
    ]
  },
  {
    id: 2,
    name: 'Programas de Asignatura',
    sections: [
      {
        id: 1,
        name: 'Bloque curricular',
        url: RUTAS_PAGINAS.BLOQUE_CURRICULAR
      },
      {
        id: 3,
        name: 'Auditoria',
        url: RUTAS_PAGINAS.AUDITORIA
      },
      {
        id: 4,
        name: 'Programas vigentes',
        url: RUTAS_PAGINAS.PROGRAMAS_VIGENTES
      },
      {
        id: 6,
        name: 'Tareas Pendientes',
        url: RUTAS_PAGINAS.TAREAS_PENDIENTES
      },
      {
        id: 7,
        name: 'Historial',
        url: RUTAS_PAGINAS.HISTORIAL
      }
    ]
  }
]

export interface Pagina {
  key: string
  title: string
  path: string
  enabled: boolean
  component: React.FC<any>
  modo?: string
}

export const PAGINAS: Pagina[] = [
  {
    key: 'inicio',
    title: 'Pagina Inicio',
    path: RUTAS_PAGINAS.INICIO,
    enabled: true,
    component: Inicio
  },
  {
    key: 'carrera',
    title: 'Carrera',
    path: RUTAS_PAGINAS.CARRERA,
    enabled: true,
    component: Carrera
  },
  {
    key: 'plan-estudio',
    title: 'Plan de Estudio',
    path: RUTAS_PAGINAS.PLAN_DE_ESTUDIO,
    enabled: true,
    component: PlanEstudio
  },
  {
    key: 'descriptores',
    title: 'Descriptores',
    path: RUTAS_PAGINAS.DESCRIPTORES,
    enabled: true,
    component: Descriptores
  },
  {
    key: 'bloque-curricular',
    title: 'Bloque Curricular',
    path: RUTAS_PAGINAS.BLOQUE_CURRICULAR,
    enabled: true,
    component: BloqueCurricular
  },
  {
    key: 'programas-vigentes',
    title: 'Programas Vigentes',
    path: RUTAS_PAGINAS.PROGRAMAS_VIGENTES,
    enabled: true,
    component: ProgramasVigentes
  },
  {
    key: 'historial',
    title: 'Historial',
    path: RUTAS_PAGINAS.HISTORIAL,
    enabled: true,
    component: Historial
  },
  {
    key: 'ver-programa-asignatura',
    title: 'Ver Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.VER
  },
  {
    key: 'nuevo-programa-asignatura',
    title: 'Nuevo Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.NUEVO}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.NUEVO
  },
  {
    key: 'editar-programa-asignatura',
    title: 'Editar Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR
  },
  {
    key: 'editar-ultimo-programa-asignatura',
    title: 'Editar Ultimo Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO
  },
  {
    key: 'auditoria',
    title: 'Auditoria',
    path: `${RUTAS_PAGINAS.AUDITORIA}`,
    enabled: true,
    component: Auditoria,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR
  },
  {
    key: 'tareas-pendientes',
    title: 'Tareas Pendientes',
    path: `${RUTAS_PAGINAS.TAREAS_PENDIENTES}`,
    enabled: true,
    component: TareasPendientes,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR
  },
  {
    key: 'editar-programa-asignatura',
    title: 'Editar Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR
  }
]

export const MENSAJES_DE_ERROR = {
  CAMPO_REQUERIDO: 'Este campo es requerido.',
  CANTIDAD_RESULTADOS_APRENDIZAJE:
    'Un programa debe tener entre 5 a 8 resultados de aprendizaje.',
  SELECCIONAR_DESCRIPTOR: 'Debe seleccionar al menos un descriptor.',
  SELECCIONAR_EJE_TRANSVERSAL: 'Debe seleccionar al menos un eje transversal.',
  SELECCIONAR_ACTIVIDAD_RESERVADA:
    'Debe seleccionar al menos una actividad reservada.'
}
