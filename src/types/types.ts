export type ProgramasAsignaturas = {
  id: number
  asignatura: string
  carrera: string
  estado: string
  id_programa: number | null
  acciones_posibles: {
    ver: boolean
    editar: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    empezar_nuevo: boolean
  }
}[]
