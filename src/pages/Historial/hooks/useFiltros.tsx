import { useState, useEffect } from 'react'
import { FiltrosType, selectedFiltrosType } from '../../../types'
import { getFiltros } from '../services'
import { ITEM_VACIO } from '../../../constants/constants'

type useHistorialType = {
  filtros: FiltrosType
  setFiltros: (filtros: FiltrosType) => void
  selectedFiltros: selectedFiltrosType
  setSelectedFiltros: (filtros: selectedFiltrosType) => void
  loadingFiltros: boolean
  errorFiltros: boolean
}

const useHistorial = (): useHistorialType => {
  const [filtros, setFiltros] = useState<FiltrosType>([])
  const [selectedFiltros, setSelectedFiltros] = useState<selectedFiltrosType>({
    carrera: ITEM_VACIO,
    asignatura: ITEM_VACIO,
    anio_lectivo: ITEM_VACIO,
    semestre: ITEM_VACIO
  })
  const [loadingFiltros, setLoading] = useState<boolean>(true)
  const [errorFiltros, setError] = useState<boolean>(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getFiltros()
        const filtrosConOpcionVacia: FiltrosType = response.map((item) => ({
          ...item,
          opciones: [ITEM_VACIO].concat(item.opciones)
        }))
        setFiltros(filtrosConOpcionVacia)
        setLoading(false)
      } catch (err) {
        setError(true)
        setLoading(false)
        setFiltros([])
      }
    }
    fetchData()
  }, [])

  return {
    filtros,
    setFiltros,
    selectedFiltros,
    setSelectedFiltros,
    loadingFiltros,
    errorFiltros
  }
}

export default useHistorial
