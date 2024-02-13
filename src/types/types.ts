export type ProgramasAsignaturas = {
  id: number
  asignatura: {
    id: number
    nombre: string
  }
  carrera: string
  estado: string
  id_programa: number | null
  acciones_posibles: {
    ver_programa: boolean
    modificar_programa: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    nuevo: boolean
  }
  accion_requerida: string | null
}[]

export type ProgramasVigentes = {
  id: number
  asignatura: {
    id: number
    nombre: string
  }
  estado: string
  id_programa: number | null
  acciones_posibles: {
    ver_programa: boolean
    modificar_programa: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    nuevo: boolean
  }
  accion_requerida: string | null
}[]

type Filtro = {
  id: number
  nombre: string
}

export type Filtros = {
  tipo: string
  nombre: string
  opciones: Filtro[]
}[]

export type selectedFiltrosType = {
  carrera: number | null | undefined
  semestre: number | null | undefined
  asignatura: number | null | undefined
  anio_lectivo: number | null | undefined
}

export type ProgramasHistorial = {
  id: number
  asignatura: {
    id: number
    nombre: string
  }
  estado: string
  id_programa: number | null
  acciones_posibles: {
    ver_programa: boolean
    modificar_programa: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    nuevo: boolean
  }
  accion_requerida: string | null
}[]
