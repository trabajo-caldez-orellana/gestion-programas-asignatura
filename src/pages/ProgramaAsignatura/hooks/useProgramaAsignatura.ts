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
  RUTAS_PAGINAS,
  MENSAJES_DE_ERROR
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

  const validarDatosPrograma = (): boolean => {
    let esFormularioValido = true
    let erroresFormulario = ERRORES_DEFAULT_PROGRAMA_ASIGNATURA

    if (!programaAsignatura.informacionAdicional.bibliografia) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          bibliografia: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.contenidos) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          contenidos: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.cronograma) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          cronograma: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.fundamentacion) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          fundamentacion: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.metodologiaAplicada) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          metodologiaAplicada: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.recursos) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          recursos: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.evaluacion) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          evaluacion: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.investigacionDocentes) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          investigacionDocentes: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.investigacionEstudiantes) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          investigacionEstudiantes: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.extensionDocentes) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          extensionDocentes: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    if (!programaAsignatura.informacionAdicional.extensionEstudiantes) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        informacionAdicional: {
          ...erroresFormulario.informacionAdicional,
          extensionEstudiantes: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
        }
      }
    }

    const cantidadResultados =
      programaAsignatura.descriptores.resultadosAprendizaje.filter(
        (item) => item !== ''
      ).length
    if (cantidadResultados < 5 || cantidadResultados > 8) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        descriptores: {
          ...erroresFormulario.descriptores,
          resultadosAprendizaje:
            MENSAJES_DE_ERROR.CANTIDAD_RESULTADOS_APRENDIZAJE
        }
      }
    }

    const cantidadDescriptores =
      programaAsignatura.descriptores.descriptores.filter(
        (item) => item.seleccionado
      ).length
    const cantidadActividadesReservadas =
      programaAsignatura.descriptores.actividadesReservadas.filter(
        (item) => item.nivel !== 0
      ).length
    const cantidadEjesTrasversales =
      programaAsignatura.descriptores.ejesTransversales.filter(
        (item) => item.nivel !== 0
      ).length

    if (cantidadActividadesReservadas === 0) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        descriptores: {
          ...erroresFormulario.descriptores,
          actividadesReservadas:
            MENSAJES_DE_ERROR.SELECCIONAR_ACTIVIDAD_RESERVADA
        }
      }
    }

    if (cantidadDescriptores === 0) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        descriptores: {
          ...erroresFormulario.descriptores,
          descriptores: MENSAJES_DE_ERROR.SELECCIONAR_DESCRIPTOR
        }
      }
    }

    if (cantidadEjesTrasversales === 0) {
      esFormularioValido = esFormularioValido && false
      erroresFormulario = {
        ...erroresFormulario,
        descriptores: {
          ...erroresFormulario.descriptores,
          ejesTransversales: MENSAJES_DE_ERROR.SELECCIONAR_EJE_TRANSVERSAL
        }
      }
    }

    setErroresProgramaAsignatura(erroresFormulario)
    return esFormularioValido
  }

  const guardarPrograma = async (presentarAprobacion: boolean) => {
    if (validarDatosPrograma()) {
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
