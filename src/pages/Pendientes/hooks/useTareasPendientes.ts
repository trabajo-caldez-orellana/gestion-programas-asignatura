import { useState, useEffect } from 'react'

import { TareaPendiente } from 'interfaces/interfaces'
import { getTareasPendientes } from '../services'

type useTareasPendientesType = {
  tareasPendientes: TareaPendiente[]
  loading: boolean
  error: boolean
  refetchTareas: () => void
}

const useTareasPendientes = (): useTareasPendientesType => {
  const [tareasPendientes, setTareasPendientes] = useState<TareaPendiente[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  const fetchData = async () => {
    try {
      const response = await getTareasPendientes()
      setTareasPendientes(response)

      setError(false)
      setLoading(false)
    } catch (err) {
      setError(true)
      setLoading(false)
    }
  }

  const refetchTareas = () => {
    fetchData()
  }

  useEffect(() => {
    fetchData()
  }, [])

  return {
    refetchTareas,
    tareasPendientes: tareasPendientes,
    loading,
    error
  }
}

export default useTareasPendientes
