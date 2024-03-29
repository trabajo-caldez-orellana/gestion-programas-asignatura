import { client } from '../../../utils/axiosClient'
import {
  ProgramasVigentes,
  FiltrosType,
  selectedFiltrosType,
  ProgramasHistorial
} from '../../../types'
import { RUTAS } from '../../../constants/constants'

export const getHistorial = async () => {
  const response = await client.get<ProgramasVigentes>(
    `${RUTAS.GET_PROGRAMAS_VIGENTES}`
  )

  return response.data
}

export const getFiltros = async () => {
  const response = await client.get<FiltrosType>(
    `${RUTAS.GET_FILTROS_HISTORIAL}`
  )

  return response.data
}

export const getSearchHistorial = async (
  selectedFiltros: selectedFiltrosType | null
) => {
  const params = `carrera=${selectedFiltros?.carrera}&semestre=${selectedFiltros?.semestre}&asignatura=${selectedFiltros?.asignatura}&anio_lectivo=${selectedFiltros?.anio_lectivo}`
  const response = await client.get<ProgramasHistorial>(
    `${RUTAS.GET_HISTORIAL}?${params}`
  )

  return response.data
}
