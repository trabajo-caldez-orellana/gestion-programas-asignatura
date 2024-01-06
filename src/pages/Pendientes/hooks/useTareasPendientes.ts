import { useState, useEffect } from 'react'

import { TareaPendiente } from 'interfaces/interfaces'
import { getTareasPendientes } from '../services'

type useTareasPendientesType = {
  tareasPendientes: TareaPendiente[]
  loading: boolean
  error: boolean
}

const useTareasPendientes = (): useTareasPendientesType => {
  const [tareasPendientes, setTareasPendientes] = useState<TareaPendiente[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  useEffect(() => {
    console.log('AAAAGH')
    const fetchData = async () => {
      try {
        const response = await getTareasPendientes()
        console.log(response)
        setTareasPendientes(response)

        setLoading(false)
      } catch (err) {
        console.error(err)
        setError(true)
      }
    }
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  })

  return {
    tareasPendientes: tareasPendientes,
    loading,
    error
  }
}

export default useTareasPendientes
