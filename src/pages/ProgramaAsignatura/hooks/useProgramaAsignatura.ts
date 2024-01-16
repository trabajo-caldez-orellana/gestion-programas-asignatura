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
  id: string | undefined,
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
      // TODO. SI el programa es nuevo, hacer un pedido distinto
      // Para las distintas opciones de descriptires
      try {
        const response = await getProgramaAsignatura(id)

        console.log(response)
        // Si el programa es nuevo debemos volver sus propiedades a su estado inicial
        if (modo === MODOS_PROGRAMA_ASIGNATURA.NUEVO) {
          response.cargaHoraria = NUEVO_PROGRAMA_ASIGNATURA.cargaHoraria
          response.informacionAdicional =
            NUEVO_PROGRAMA_ASIGNATURA.informacionAdicional
          response.descriptores.descriptores.forEach((descriptor) => {
            descriptor.seleccionado = false
          })
          response.descriptores.ejesTransversales.forEach((eje) => {
            eje.nivel = 0
          })
        }
        setProgramaAsignatura(response)
        setLoading(false)
      } catch (err) {
        console.error(err)
        setError(true)
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
