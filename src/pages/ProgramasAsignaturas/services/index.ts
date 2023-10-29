import axios from 'axios'
import { ProgramaAsignatura } from '../../../interfaces'



export const getProgramaAsignatura = async (id: string | undefined) => {
  const response = await axios.get<ProgramaAsignatura>(
    `/programa-asignaturas/${id}`
  )

  return response.data
}
