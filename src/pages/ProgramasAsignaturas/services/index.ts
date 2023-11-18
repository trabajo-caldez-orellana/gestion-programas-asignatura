import axios from 'axios'
import { ProgramaAsignatura } from '../../../interfaces'
import { ProgramasAsignaturas } from '../../../types'
import { RUTAS } from '../../../constants/constants'

export const getProgramaAsignatura = async (id: string | undefined) => {
  const response = await axios.get<ProgramaAsignatura>(
    `${RUTAS.GET_PROGRAMA_ASIGNATURA}/${id}`
  )

  return response.data
}

export const getProgramasAsignaturas = async () => {
  const response = await axios.get<ProgramasAsignaturas>(
    `${RUTAS.GET_PROGRAMAS_ASIGNATURAS}`
  )

  return response.data
}

export const postProgramaAsignatura = async (
  programaAsignatura: ProgramaAsignatura | null,
  isDraft: boolean
) => {
  const response = await axios.post(`${RUTAS.POST_PROGRAMAS_ASIGNATURAS}/${programaAsignatura?.id}`, {
    programaAsignatura,
    isDraft
  })

  return response.data
}
