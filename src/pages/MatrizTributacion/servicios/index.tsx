import { RUTAS } from '../../../constants/constants'
import { client } from '../../../utils/axiosClient'

import {
  MatrizAPIErrorInterface,
  MatrizErroresInterface,
  PlanesDeEstudioAPIBody,
  PlanesDeEstudioInterface
} from 'interfaces/interfaces'

const parsePlanesDeEstudio = (
  planes: PlanesDeEstudioAPIBody[]
): PlanesDeEstudioInterface[] => {
  return planes.map((plan) => {
    return {
      id: plan.id,
      nombre: plan.nombre,
      carreraId: plan.carrera_id,
      carreraNombre: plan.nombre_carrera
    }
  })
}

export const getPlanesDeEstudio = async () => {
  try {
    const response = await client.get(`${RUTAS.GET_PLANES_DE_ESTUDIO}`)
    return {
      status: response.status,
      data: parsePlanesDeEstudio(response.data.data)
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    return {
      status: err.response.status
    }
  }
}

const parseMatrizErrors = (
  error: MatrizAPIErrorInterface
): MatrizErroresInterface => {
  return {
    all: error.__all__ ? error.__all__[0] : '',
    planDeEstudio: error.plan_de_estudio ? error.plan_de_estudio[0] : '',
    carrera: error.carrera ? error.carrera[0] : ''
  }
}

export const getMatrizDeTributacion = async (
  idPlanDeEstudio: number,
  idCarrera: number
) => {
  try {
    const response = await client.get(
      `${RUTAS.GET_MATRIZ_DE_TRIBUTACION}${idCarrera}/${idPlanDeEstudio}/`,
      { headers: { 'Content-Type': 'text/csv' } }
    )
    return {
      status: response.status,
      data: response.data
    }
  } catch (err: any) {
    return {
      status: err.response.status,
      error: parseMatrizErrors(err.response.data.error)
    }
  }
}
