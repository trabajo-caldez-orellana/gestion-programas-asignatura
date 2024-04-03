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
  selectedFiltros: selectedFiltrosType
) => {
  let params = ''

  if (selectedFiltros.carrera.id !== -1) {
    params += `carrera=${selectedFiltros.carrera.id}&`
  }

  if (selectedFiltros.semestre.id !== -1) {
    params += `semestre=${selectedFiltros.semestre.id}&`
  }

  if (selectedFiltros.asignatura.id !== -1) {
    params += `asignatura=${selectedFiltros.asignatura.id}&`
  }

  if (selectedFiltros.anio_lectivo.id !== -1) {
    params += `anio_lectivo=${selectedFiltros.anio_lectivo.id}&`
  }

  if (params[params.length - 1] === '&') {
    params = params.slice(0, -1)
  }

  const response = await client.get<ProgramasHistorial>(
    `${RUTAS.GET_HISTORIAL}?${params}`
  )

  return response.data
}
