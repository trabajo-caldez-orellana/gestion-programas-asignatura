import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  ProgramaAsignatura,
  ProgramaAsignaturaErrores
} from 'interfaces/interfaces'
import {
  getProgramaAsignatura,
  getInformacionParaModificacion,
  getInformacionNuevoPrograma,
  getInformacionModificarAPartirUltimo,
  crearProgramaAsignatura,
  modificarProgramaAsignatura
} from '../services'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  NUEVO_PROGRAMA_ASIGNATURA,
  ERRORES_DEFAULT_PROGRAMA_ASIGNATURA,
  RUTAS_PAGINAS
} from '../../../constants/constants'

type useProgramaAsignaturaType = {
  programaAsignatura: ProgramaAsignatura
  setProgramaAsignatura: React.Dispatch<
    React.SetStateAction<ProgramaAsignatura>
  >
  erroresProgramaAsignatura: ProgramaAsignaturaErrores
  guardarPrograma: (presentarAprobacion: boolean) => void
  modoProgramaAsignatura: string
  loading: boolean
  errorInesperado: string
}

const MENSAJE_ERROR_INESPERADO =
  'Algo inesperado ha ocurrido. Intente nuevamente más tarde.'

const useProgramaAsignatura = (
  id: string = '',
  modo: string | null
): useProgramaAsignaturaType => {
  const [programaAsignatura, setProgramaAsignatura] =
    useState<ProgramaAsignatura>(NUEVO_PROGRAMA_ASIGNATURA)
  const [erroresProgramaAsignatura, setErroresProgramaAsignatura] =
    useState<ProgramaAsignaturaErrores>(ERRORES_DEFAULT_PROGRAMA_ASIGNATURA)
  // Persistimos el modo, por defecto es VER
  const [modoProgramaAsignatura, setModoProgramaAsignatura] = useState<string>(
    MODOS_PROGRAMA_ASIGNATURA.VER
  )
  const [loading, setLoading] = useState<boolean>(true)
  const [errorInesperado, setErrorInesperado] = useState<string>('')
  const navigate = useNavigate()

  const guardarPrograma = async (presentarAprobacion: boolean) => {
    if (
      modo === MODOS_PROGRAMA_ASIGNATURA.NUEVO ||
      modo === MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO
    ) {
      const response = await crearProgramaAsignatura(
        programaAsignatura,
        presentarAprobacion,
        parseInt(id)
      )

      if (response.status === 200) {
        navigate(RUTAS_PAGINAS.TAREAS_PENDIENTES)
        return
      }

      if (response.error) {
        setErroresProgramaAsignatura(response.error)
      }
    } else {
      const response = await modificarProgramaAsignatura(
        programaAsignatura,
        presentarAprobacion,
        parseInt(id)
      )

      if (response.status === 200) {
        navigate(RUTAS_PAGINAS.TAREAS_PENDIENTES)
        return
      }

      if (response.error) {
        setErroresProgramaAsignatura(response.error)
      }
    }
  }

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
        const datosNuevoPrograma = NUEVO_PROGRAMA_ASIGNATURA

        try {
          const response = await getInformacionNuevoPrograma(id)
          if (response.status === 200 && response.data) {
            datosNuevoPrograma.descriptores = {
              ...NUEVO_PROGRAMA_ASIGNATURA.descriptores,
              actividadesReservadas: response.data?.actividadesReservadas,
              ejesTransversales: response.data?.ejesTransversales,
              descriptores: response.data?.descriptores
            }
            setProgramaAsignatura(datosNuevoPrograma)
          } else if (response.status !== 200 && response.error) {
            setErrorInesperado(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setLoading(false)
        } catch (err) {
          setErrorInesperado(MENSAJE_ERROR_INESPERADO)
        }

        setProgramaAsignatura(NUEVO_PROGRAMA_ASIGNATURA)
        setLoading(false)
      } else if (modo === MODOS_PROGRAMA_ASIGNATURA.VER) {
        try {
          const response = await getProgramaAsignatura(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else if (response.status !== 200 && response.error) {
            setErrorInesperado(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setLoading(false)
        } catch (err) {
          setErrorInesperado(MENSAJE_ERROR_INESPERADO)
        }
      } else if (modo === MODOS_PROGRAMA_ASIGNATURA.EDITAR) {
        try {
          const response = await getInformacionParaModificacion(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else if (response.status !== 200 && response.error) {
            setErrorInesperado(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setLoading(false)
        } catch (err) {
          setErrorInesperado(MENSAJE_ERROR_INESPERADO)
        }
      } else {
        try {
          const response = await getInformacionModificarAPartirUltimo(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else if (response.status !== 200 && response.error) {
            setErrorInesperado(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setLoading(false)
        } catch (err) {
          setErrorInesperado(MENSAJE_ERROR_INESPERADO)
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
    erroresProgramaAsignatura,
    loading,
    errorInesperado,
    guardarPrograma
  }
}

export default useProgramaAsignatura
