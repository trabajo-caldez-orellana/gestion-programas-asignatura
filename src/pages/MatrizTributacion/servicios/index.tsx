import { RUTAS } from 'constants/constants'
import { client } from 'utils/axiosClient'

import {
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
      carreraNombre: plan.carrera_nombre
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
