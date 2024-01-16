import { useState, useEffect } from 'react'
import { ProgramasAsignaturas } from '../../../types'
import { getProgramasAsignaturas } from '../services'

type useProgramasAsignaturasType = {
  programasAsignaturas: ProgramasAsignaturas | null
  loading: boolean
  error: boolean
}

const useProgramaAsignatura = (): useProgramasAsignaturasType => {
  const [programasAsignaturas, setProgramasAsignaturas] =
    useState<ProgramasAsignaturas | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getProgramasAsignaturas()
        setProgramasAsignaturas(response)
        setLoading(false)
      } catch (err) {
        console.error(err)
        setError(true)
      }
    }
    fetchData()
  }, [])

  return { programasAsignaturas, loading, error }
}

export default useProgramaAsignatura
