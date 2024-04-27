import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores
} from 'interfaces/interfaces'

import {
  Inicio,
  Historial,
  ProgramaAsignatura,
  TareasPendientes,
  ProgramasVigentes,
  Login,
  Matriz,
  LoginLoading
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
  POST_EDITAR_PROGRAMA_ASIGNATURA: 'api/programas/editar/',
  GET_PLANES_DE_ESTUDIO: 'api/planes-de-esutdio/',
  GET_MATRIZ_DE_TRIBUTACION: 'api/informes/matriz/',
  REUTILIZAR_ULTIMO_PROGRAMA:
    'api/informacion-formularios/reutilizar-programa/',
  APROBAR_PROGRAMA: 'api/programas/aprobar/',
  PEDIR_CAMBIOS_PROGRAMA: 'api/programas/pedir_cambios/',
  OBTENER_CORRELATIVAS_DISPONIBLES_PROGRAMA:
    'api/opciones/asignaturas-correlativas-programa/',
  OBTENER_CORRELATIVAS_DISPONIBLES_ASIGNATURA:
    'api/opciones/asignaturas-correlativas/'
}

export const HANDLERS = {
  GET_PROGRAMA_ASIGNATURA_HANDLER: '/programa-asignatura/:id',
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
  EDITAR_ULTIMO: 'editar-ultimo',
  IMPRIMIR: 'imprimir',
  REVISAR: 'revisar'
}

export const NUEVO_PROGRAMA_ASIGNATURA: ProgramaAsignaturaInterface = {
  id: 1,
  informacionGeneral: {
    nombreAsignatura: '',
    codigoAsignatura: '',
    carreras: [],
    equipoDocente: [],
    anioAcademico: '',
    bloqueCurricular: ''
  },
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
    ejesTransversales: [],
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
  },
  correlativas: []
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
  correlativas: '',
  all: '',
  mensaje: ''
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

export const enum ROLES {
  DOCENTE = 'D',
  DIRECTOR = 'DI',
  SECRETARIO = 'S'
}

export interface SidebarSection {
  id: number
  name: string
  sections: {
    id: number
    name: string
    url: string
    permisos: ROLES[] | null
  }[]
}

export const RUTAS_PAGINAS = {
  PROGRAMA_DE_ASIGNATURA: '/programa-asignatura',
  PROGRAMAS_VIGENTES: '/programas-vigentes',
  TAREAS_PENDIENTES: '/tareas-pendientes',
  HISTORIAL: '/historial',
  LOGIN: '/login',
  MATRIZ: '/matriz-tributacion',
  LOGIN_LOADING: '/login-loading',
  INICIO: ''
}

export const SIDEBAR_SECTIONS: SidebarSection[] = [
  {
    id: 1,
    name: 'Informes',
    sections: [
      {
        id: 1,
        name: 'Matriz de Tributación',
        url: RUTAS_PAGINAS.MATRIZ,
        permisos: [ROLES.DIRECTOR, ROLES.SECRETARIO]
      }
    ]
  },
  {
    id: 2,
    name: 'Programas de Asignatura',
    sections: [
      {
        id: 4,
        name: 'Programas vigentes',
        url: RUTAS_PAGINAS.PROGRAMAS_VIGENTES,
        permisos: null
      },
      {
        id: 6,
        name: 'Tareas Pendientes',
        url: RUTAS_PAGINAS.TAREAS_PENDIENTES,
        permisos: [ROLES.DOCENTE, ROLES.DIRECTOR]
      },
      {
        id: 7,
        name: 'Historial',
        url: RUTAS_PAGINAS.HISTORIAL,
        permisos: null
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
  protectedByLogin: boolean
}

export const PAGINAS: Pagina[] = [
  {
    key: 'programas-vigentes',
    title: 'Programas Vigentes',
    path: RUTAS_PAGINAS.PROGRAMAS_VIGENTES,
    enabled: true,
    component: ProgramasVigentes,
    protectedByLogin: true
  },
  {
    key: 'historial',
    title: 'Historial',
    path: RUTAS_PAGINAS.HISTORIAL,
    enabled: true,
    component: Historial,
    protectedByLogin: true
  },
  {
    key: 'ver-programa-asignatura',
    title: 'Ver Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.VER,
    protectedByLogin: true
  },
  {
    key: 'nuevo-programa-asignatura',
    title: 'Nuevo Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.NUEVO}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.NUEVO,
    protectedByLogin: true
  },
  {
    key: 'editar-programa-asignatura',
    title: 'Editar Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR,
    protectedByLogin: true
  },
  {
    key: 'editar-ultimo-programa-asignatura',
    title: 'Editar Ultimo Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO,
    protectedByLogin: true
  },
  {
    key: 'revisar-programa-de-asignatura',
    title: 'Revisar Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.REVISAR}/:id`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.REVISAR,
    protectedByLogin: true
  },
  {
    key: 'tareas-pendientes',
    title: 'Tareas Pendientes',
    path: `${RUTAS_PAGINAS.TAREAS_PENDIENTES}`,
    enabled: true,
    component: TareasPendientes,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR,
    protectedByLogin: true
  },
  {
    key: 'editar-programa-asignatura',
    title: 'Editar Programa Asignatura',
    path: `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}`,
    enabled: true,
    component: ProgramaAsignatura,
    modo: MODOS_PROGRAMA_ASIGNATURA.EDITAR,
    protectedByLogin: true
  },
  {
    key: 'login',
    title: 'Iniciar Sesion',
    path: RUTAS_PAGINAS.LOGIN,
    enabled: true,
    component: Login,
    protectedByLogin: false
  },
  {
    key: 'matriz-tributacion',
    title: 'Matriz de Tributación',
    path: RUTAS_PAGINAS.MATRIZ,
    enabled: true,
    component: Matriz,
    protectedByLogin: true
  },
  {
    key: 'login-loading',
    title: 'Cargando',
    enabled: true,
    path: RUTAS_PAGINAS.LOGIN_LOADING,
    component: LoginLoading,
    protectedByLogin: false
  },
  {
    key: 'inicio',
    title: 'Pagina Inicio',
    path: RUTAS_PAGINAS.INICIO,
    enabled: true,
    component: Inicio,
    protectedByLogin: false
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

export interface DatoListaInterface {
  id: number
  informacion: string
}

export interface DatosListaSeleccionInterface extends DatoListaInterface {
  seleccionado: boolean
}

export interface ModalProps {
  open: boolean
  children: React.ReactNode
  modalTitle?: string
  onClose: () => void
}

export const enum TIPO_CORRELATIVA {
  NO_SELECCIONADO = '-',
  REGULAR = 'R',
  APROBADO = 'A'
}

export const enum REQUISITOS_CORRELATIVA {
  ASIGNATURA = 'asignatura',
  CANTIDAD_ASIGNATURAS = 'cantidad',
  MODULO = 'modulo'
}

export const LISTADO_SELECCION_TIPOS_CORRELATIVA = [
  {
    id: TIPO_CORRELATIVA.NO_SELECCIONADO,
    informacion: 'Seleccione Tipo de Correlativa'
  },
  { id: TIPO_CORRELATIVA.APROBADO, informacion: 'Aprobado' },
  { id: TIPO_CORRELATIVA.REGULAR, informacion: 'Regular' }
]

export const ITEM_VACIO: DatoListaInterface = {
  id: -1,
  informacion: 'Seleccionar filtro'
}

export const ASIGNATURA_VACIA: DatoListaInterface = {
  id: -1,
  informacion: ''
}
