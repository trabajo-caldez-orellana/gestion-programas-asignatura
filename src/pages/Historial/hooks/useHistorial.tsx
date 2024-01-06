import { useState, useEffect } from 'react'
import { ProgramasVigentes } from '../../../types'
import { getHistorial } from '../services'

type useHistorialType = {
  programasVigentes: ProgramasVigentes | null
  loading: boolean
  error: boolean
}

const useHistorial = (): useHistorialType => {
  const [programasVigentes, setProgramasVigentes] =
    useState<ProgramasVigentes | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getHistorial()
        setProgramasVigentes(response)
        setLoading(false)
      } catch (err) {
        console.error(err)
        setError(true)
      }
    }
    fetchData()
  }, [])

  return { programasVigentes, loading, error }
}

export default useHistorial
