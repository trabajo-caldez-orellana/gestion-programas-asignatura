import { useState, useEffect } from 'react'
import { ProgramasVigentes } from '../../../types'
import { getProgramasVigentes } from '../services'

type useProgramasVigentesType = {
  programasVigentes: ProgramasVigentes | null
  loading: boolean
  error: boolean
}

const useProgramasVigentes = (): useProgramasVigentesType => {
  const [programasVigentes, setProgramasVigentes] =
    useState<ProgramasVigentes | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getProgramasVigentes()
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

export default useProgramasVigentes
