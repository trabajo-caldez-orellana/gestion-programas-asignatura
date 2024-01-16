import { MODOS_PROGRAMA_ASIGNATURA } from '../constants/constants'
import { useNavigate } from 'react-router-dom'

export const useVerPrograma = () => {
  const navigate = useNavigate()

  const verPrograma = (id: number | null, modoPrograma: string) => {
    const rutaBase = `/programa-asignaturas`

    switch (modoPrograma) {
      case MODOS_PROGRAMA_ASIGNATURA.VER:
        navigate(`${rutaBase}/${id}`)
        break
      case MODOS_PROGRAMA_ASIGNATURA.EDITAR:
        navigate(`${rutaBase}/editar/${id}`)
        break
      case MODOS_PROGRAMA_ASIGNATURA.NUEVO:
        navigate(`${rutaBase}/nuevo/${id}`)
        break
      default:
    }
  }

  return { verPrograma }
}
