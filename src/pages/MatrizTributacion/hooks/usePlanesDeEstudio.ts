import { useState, useEffect } from 'react'
import { PlanesDeEstudioInterface } from 'interfaces/interfaces'
import { getPlanesDeEstudio } from '../servicios'

type usePlanesDeEstudioType = {
  planesDeEstudio: PlanesDeEstudioInterface[]
  loading: boolean
  error: string
}

const MENSAJE_ERROR_INESPERADO =
  'Algo inesperado ha ocurrido. Intente nuevamente más tarde.'

const usePlanesDeEstudio = (): usePlanesDeEstudioType => {
  const [loading, setLoading] = useState<boolean>(true)
  const [planesDeEstudio, setPlanesDeEstudio] = useState<
    PlanesDeEstudioInterface[]
  >([])
  const [error, setError] = useState<string>('')

  const obtenerPlanesDeEstudio = async () => {
    setLoading(true)
    const response = await getPlanesDeEstudio()
    if (response.status === 200 && response.data) {
      setPlanesDeEstudio(response.data)
      setError('')
      setLoading(false)
    } else {
      setError(MENSAJE_ERROR_INESPERADO)
      setLoading(false)
    }
  }

  useEffect(() => {
    obtenerPlanesDeEstudio()
  }, [])

  return {
    planesDeEstudio,
    loading,
    error
  }
}

export default usePlanesDeEstudio
