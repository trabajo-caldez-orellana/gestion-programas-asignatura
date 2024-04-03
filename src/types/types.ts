import { DatoListaInterface } from '../constants/constants'

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

export type FiltrosType = {
  tipo: 'carrera' | 'semestre' | 'asignatura' | 'anio_lectivo'
  nombre: string
  opciones: DatoListaInterface[]
}[]

export type selectedFiltrosType = {
  carrera: DatoListaInterface
  semestre: DatoListaInterface
  asignatura: DatoListaInterface
  anio_lectivo: DatoListaInterface
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
