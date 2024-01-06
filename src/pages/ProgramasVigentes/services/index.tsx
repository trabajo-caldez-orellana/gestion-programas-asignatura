import { client } from '../../../utils/axiosClient'
import { ProgramasVigentes } from '../../../types'
import { RUTAS } from '../../../constants/constants'

export const getProgramasVigentes = async () => {
  const response = await client.get<ProgramasVigentes>(
    `${RUTAS.GET_PROGRAMAS_VIGENTES}`
  )

  return response.data
}
