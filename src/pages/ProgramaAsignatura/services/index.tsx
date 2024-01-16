import { client } from '../../../utils/axiosClient'
import { ProgramaAsignatura } from '../../../interfaces'
import { ProgramasAsignaturas } from '../../../types'
import { RUTAS } from '../../../constants/constants'

export const getProgramaAsignatura = async (id: string | undefined) => {
  const response = await client.get<ProgramaAsignatura>(
    `${RUTAS.GET_PROGRAMA_ASIGNATURA}${id}/`
  )

  return response.data
}

// TODO. Esto creo que se va a eliminar proximamente....
export const getProgramasAsignaturas = async () => {
  const response = await client.get<ProgramasAsignaturas>(
    `${RUTAS.GET_PROGRAMAS_ASIGNATURAS}`
  )

  return response.data
}

// TODO. Esto creo que se va a eliminar proximamente....
export const postProgramaAsignatura = async (
  programaAsignatura: ProgramaAsignatura | null,
  isDraft: boolean
) => {
  const response = await client.post(
    `${RUTAS.POST_PROGRAMAS_ASIGNATURAS}/${programaAsignatura?.id}`,
    {
      programaAsignatura,
      isDraft
    }
  )

  return response.data
}
