import { client } from '../../../utils/axiosClient'

import { RUTAS } from '../../../constants/constants'
import { TareaPendiente } from 'interfaces/interfaces'

interface DatosAsignaturaTareaPendienteAPI {
  id: number
  denominacion: string
}

interface AccionesPosiblesInterfaceAPI {
  ver_programa: boolean
  modificar_programa: boolean
  reutilizar_ultimo: boolean
  modificar_ultimo: boolean
  nuevo: boolean
}

interface TareaPendienteAPI {
  asignatura: DatosAsignaturaTareaPendienteAPI
  id_programa: number | null
  accion_requerida: string
  acciones_posibles: AccionesPosiblesInterfaceAPI
}

const parserTareasPendientes = (
  data: TareaPendienteAPI[]
): TareaPendiente[] => {
  return data.map((tarea) => {
    return {
      asignatura: {
        id: tarea.asignatura.id,
        nombre: tarea.asignatura.denominacion
      },
      idPrograma: tarea.id_programa,
      accionRequerida: tarea.accion_requerida,
      accionesPosibles: {
        verPrograma: tarea.acciones_posibles.ver_programa,
        modificarPrograma: tarea.acciones_posibles.modificar_programa,
        reutilizarUltimo: tarea.acciones_posibles.reutilizar_ultimo,
        modificarUltimo: tarea.acciones_posibles.modificar_ultimo,
        nuevo: tarea.acciones_posibles.nuevo
      }
    }
  })
}

export const getTareasPendientes = async (): Promise<TareaPendiente[]> => {
  const response = await client.get(`${RUTAS.GET_TAREAS_PENDIENTES}`)

  return parserTareasPendientes(response.data.data)
}
