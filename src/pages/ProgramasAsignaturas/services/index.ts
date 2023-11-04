import axios from 'axios'
import { ProgramaAsignatura } from '../../../interfaces'
import { RUTAS } from '../../../constants/constants'



export const getProgramaAsignatura = async (id: string | undefined) => {
  const response = await axios.get<ProgramaAsignatura>(
    `${RUTAS.GET_PROGRAMA_ASIGNATURA}/${id}`
  )

  return response.data
}
