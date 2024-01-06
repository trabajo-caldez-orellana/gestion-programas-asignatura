export type tableRowProgramasVigentes = {
  id: number | null
  asignatura: {
    id: number
    nombre: string
  }
  estado: string
  acciones_posibles: {
    ver_programa: boolean
    modificar_programa: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    nuevo: boolean
    imprimir?: boolean
  }
  accion_requerida: string | null
}
