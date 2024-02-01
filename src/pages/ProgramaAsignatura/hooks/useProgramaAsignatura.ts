import { useState, useEffect } from 'react'
import { ProgramaAsignatura } from 'interfaces'
import { getProgramaAsignatura } from '../services'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  NUEVO_PROGRAMA_ASIGNATURA
} from '../../../constants/constants'

type useProgramaAsignaturaType = {
  programaAsignatura: ProgramaAsignatura | null
  setProgramaAsignatura: React.Dispatch<
    React.SetStateAction<ProgramaAsignatura | null>
  >
  modoProgramaAsignatura: string
  loading: boolean
  error: boolean
}

const useProgramaAsignatura = (
  id: string = '',
  modo: string | null
): useProgramaAsignaturaType => {
  const [programaAsignatura, setProgramaAsignatura] =
    useState<ProgramaAsignatura | null>(null)
  // Persistimos el modo, por defecto es VER
  const [modoProgramaAsignatura, setModoProgramaAsignatura] = useState<string>(
    MODOS_PROGRAMA_ASIGNATURA.VER
  )
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  useEffect(
    () => {
      // Persistimos el modo en el que se encuentra el programa
      if (modo) {
        setModoProgramaAsignatura(modo)
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  )

  useEffect(() => {
    const fetchData = async (modo: string | null) => {
      if (modo === MODOS_PROGRAMA_ASIGNATURA.NUEVO) {
        // TODO. Cuando es nuevo programa, deberia traer datos de los descriptores posibles y eso!!!
        setProgramaAsignatura(NUEVO_PROGRAMA_ASIGNATURA)
        setLoading(false)
      } else {
        try {
          const response = await getProgramaAsignatura(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else {
            setError(true)
          }
          setLoading(false)
        } catch (err) {
          setError(true)
        }
      }
    }

    fetchData(modo)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  return {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    loading,
    error
  }
}

export default useProgramaAsignatura
