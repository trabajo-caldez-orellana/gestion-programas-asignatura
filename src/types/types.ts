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
