import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores
} from 'interfaces/interfaces'
import {
  getProgramaAsignatura,
  getInformacionParaModificacion,
  getInformacionNuevoPrograma,
  getInformacionModificarAPartirUltimo,
  crearProgramaAsignatura,
  modificarProgramaAsignatura,
  aprobarProgramaAsignatura,
  pedirCambiosProgramaAsignatura,
  obtenerAsignaturasDisponiblesAPartirDeAsignatura,
  obtenerAsignaturasDisponiblesAPartirDePrograma
} from '../services'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  NUEVO_PROGRAMA_ASIGNATURA,
  ERRORES_DEFAULT_PROGRAMA_ASIGNATURA,
  RUTAS_PAGINAS,
  MENSAJES_DE_ERROR,
  DatoListaInterface,
  TIPO_CORRELATIVA,
  REQUISITOS_CORRELATIVA,
  ASIGNATURA_VACIA
} from '../../../constants/constants'

type useProgramaAsignaturaType = {
  cargandoPrograma: boolean
  errorCargandoPrograma: string
  modoProgramaAsignatura: string
  programaAsignatura: ProgramaAsignaturaInterface
  erroresProgramaAsignatura: ProgramaAsignaturaErrores
  setProgramaAsignatura: React.Dispatch<
    React.SetStateAction<ProgramaAsignaturaInterface>
  >
  guardarPrograma: (presentarAprobacion: boolean) => void
  aprobarPrograma: () => void
  pedirCambiosPrograma: (mensaje: string) => void
  accionEnProgreso: boolean
  asignaturasDisponibles: DatoListaInterface[]
}

const MENSAJE_ERROR_INESPERADO =
  'Algo inesperado ha ocurrido. Intente nuevamente más tarde.'

const useProgramaAsignatura = (
  id: string = '',
  modo: string | null
): useProgramaAsignaturaType => {
  const [asignaturasDisponibles, setAsignaturasDisponibles] = useState<
    DatoListaInterface[]
  >([])
  const [programaAsignatura, setProgramaAsignatura] =
    useState<ProgramaAsignaturaInterface>(NUEVO_PROGRAMA_ASIGNATURA)
  const [erroresProgramaAsignatura, setErroresProgramaAsignatura] =
    useState<ProgramaAsignaturaErrores>(ERRORES_DEFAULT_PROGRAMA_ASIGNATURA)
  // Persistimos el modo, por defecto es VER
  const [modoProgramaAsignatura, setModoProgramaAsignatura] = useState<string>(
    MODOS_PROGRAMA_ASIGNATURA.VER
  )
  const [cargandoPrograma, setCargandoPrograma] = useState<boolean>(true)
  const [accionEnProgreso, setAccionEnProgreso] = useState<boolean>(false)
  const [errorCargandoPrograma, setErrorCargandoPrograma] = useState<string>('')
  const navigate = useNavigate()

  const validarDatosPrograma = (): boolean => {
    let esFormularioValido = true
    let erroresFormulario = ERRORES_DEFAULT_PROGRAMA_ASIGNATURA

    const camposTextoRequeridos = [
      'bibliografia',
      'contenidos',
      'cronograma',
      'fundamentacion',
      'metodologiaAplicada',
      'recursos',
      'evaluacion',
      'investigacionDocentes',
      'investigacionEstudiantes',
      'extensionDocentes',
      'extensionEstudiantes'
    ]

    camposTextoRequeridos.forEach((campo) => {
      if (!programaAsignatura.informacionAdicional[campo]) {
        esFormularioValido = false
        erroresFormulario = {
          ...erroresFormulario,
          informacionAdicional: {
            ...erroresFormulario.informacionAdicional,
            [campo]: MENSAJES_DE_ERROR.CAMPO_REQUERIDO
          }
        }
      }
    })

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

    programaAsignatura.correlativas.forEach((correlativa) => {
      if (correlativa.tipo === TIPO_CORRELATIVA.NO_SELECCIONADO) {
        esFormularioValido = esFormularioValido && false
        erroresFormulario = {
          ...erroresFormulario,
          correlativas: 'El tipo de correlativa es requerido.'
        }
      }

      if (
        correlativa.requisito === REQUISITOS_CORRELATIVA.ASIGNATURA &&
        correlativa.asignatura === ASIGNATURA_VACIA
      ) {
        esFormularioValido = esFormularioValido && false
        erroresFormulario = {
          ...erroresFormulario,
          correlativas:
            'Es requerido elegir la asignatura para una asignatura correlativa.'
        }
      }

      if (
        correlativa.requisito === REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS &&
        (!correlativa.cantidadAsignaturas ||
          correlativa.cantidadAsignaturas <= 0)
      ) {
        esFormularioValido = esFormularioValido && false
        erroresFormulario = {
          ...erroresFormulario,
          correlativas:
            'Es requerido indicar la cantidad de asignaturas para la correlativa de cantidad de asignaturas.'
        }
      }

      if (
        correlativa.requisito === REQUISITOS_CORRELATIVA.MODULO &&
        !correlativa.modulo
      ) {
        esFormularioValido = esFormularioValido && false
        erroresFormulario = {
          ...erroresFormulario,
          correlativas:
            'Es requerido indicar el módulo para la correlativa de módulo.'
        }
      }
    })

    setErroresProgramaAsignatura(erroresFormulario)
    return esFormularioValido
  }

  const aprobarPrograma = async () => {
    const response = await aprobarProgramaAsignatura(parseInt(id))
    setAccionEnProgreso(true)

    if (response.status !== 200 && response.error) {
      setErroresProgramaAsignatura(response.error)
      setAccionEnProgreso(false)
      return
    }

    if (response.status === 200) {
      navigate(RUTAS_PAGINAS.TAREAS_PENDIENTES)
      setAccionEnProgreso(false)
    }

    setAccionEnProgreso(false)
  }

  const pedirCambiosPrograma = async (mensaje: string) => {
    const response = await pedirCambiosProgramaAsignatura(parseInt(id), mensaje)
    setAccionEnProgreso(true)

    if (response.status !== 200 && response.error) {
      setAccionEnProgreso(false)
      setErroresProgramaAsignatura(response.error)
      return
    }

    if (response.status === 200) {
      navigate(RUTAS_PAGINAS.TAREAS_PENDIENTES)
      setAccionEnProgreso(false)
    }

    setAccionEnProgreso(false)
  }

  const guardarPrograma = async (presentarAprobacion: boolean) => {
    setAccionEnProgreso(true)
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
          setAccionEnProgreso(false)
          return
        }

        if (response.error) {
          setErroresProgramaAsignatura(response.error)
          setAccionEnProgreso(false)
        }
      } else {
        const response = await modificarProgramaAsignatura(
          programaAsignatura,
          presentarAprobacion,
          parseInt(id)
        )

        if (response.status === 200) {
          navigate(RUTAS_PAGINAS.TAREAS_PENDIENTES)
          setAccionEnProgreso(false)
          return
        }

        if (response.error) {
          setErroresProgramaAsignatura(response.error)
          setAccionEnProgreso(false)
        }
      }
    }
    setAccionEnProgreso(false)
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
            datosNuevoPrograma.informacionGeneral =
              response.data.informacionGeneral
            datosNuevoPrograma.cargaHoraria = response.data.cargaHoraria
          } else if (response.status !== 200 && response.error) {
            setErrorCargandoPrograma(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setCargandoPrograma(false)
        } catch (err) {
          setErrorCargandoPrograma(MENSAJE_ERROR_INESPERADO)
        }

        setProgramaAsignatura(NUEVO_PROGRAMA_ASIGNATURA)
        setCargandoPrograma(false)
      } else if (
        modo === MODOS_PROGRAMA_ASIGNATURA.VER ||
        modo === MODOS_PROGRAMA_ASIGNATURA.REVISAR
      ) {
        try {
          const response = await getProgramaAsignatura(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else if (response.status !== 200 && response.error) {
            setErrorCargandoPrograma(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setCargandoPrograma(false)
        } catch (err) {
          setErrorCargandoPrograma(MENSAJE_ERROR_INESPERADO)
        }
      } else if (modo === MODOS_PROGRAMA_ASIGNATURA.EDITAR) {
        try {
          const response = await getInformacionParaModificacion(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else if (response.status !== 200 && response.error) {
            setErrorCargandoPrograma(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setCargandoPrograma(false)
        } catch (err) {
          setErrorCargandoPrograma(MENSAJE_ERROR_INESPERADO)
        }
      } else {
        try {
          const response = await getInformacionModificarAPartirUltimo(id)
          if (response.status === 200 && response.data) {
            setProgramaAsignatura(response.data)
          } else if (response.status !== 200 && response.error) {
            setErrorCargandoPrograma(response.error || MENSAJE_ERROR_INESPERADO)
          }
          setCargandoPrograma(false)
        } catch (err) {
          setErrorCargandoPrograma(MENSAJE_ERROR_INESPERADO)
        }
      }
    }

    fetchData(modo)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  useEffect(() => {
    if (
      modo === MODOS_PROGRAMA_ASIGNATURA.NUEVO ||
      modo === MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO
    ) {
      obtenerAsignaturasDisponiblesAPartirDeAsignatura(id).then((response) => {
        setAsignaturasDisponibles(response.data)
      })
    } else if (modo === MODOS_PROGRAMA_ASIGNATURA.EDITAR) {
      obtenerAsignaturasDisponiblesAPartirDePrograma(id).then((response) => {
        setAsignaturasDisponibles(response.data)
      })
    } else {
      setAsignaturasDisponibles([])
    }
  }, [modo])

  return {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    erroresProgramaAsignatura,
    cargandoPrograma,
    errorCargandoPrograma,
    guardarPrograma,
    aprobarPrograma,
    pedirCambiosPrograma,
    accionEnProgreso,
    asignaturasDisponibles
  }
}

export default useProgramaAsignatura
