import { useState, useEffect } from 'react'
import { ProgramaAsignatura } from '../../../interfaces'
import { getProgramaAsignatura } from '../services'

type useProgramaAsignaturaType = {
  programaAsignatura: ProgramaAsignatura | null
  setProgramaAsignatura: React.Dispatch<
    React.SetStateAction<ProgramaAsignatura | null>
  >
  loading: boolean
  error: boolean
}

const useProgramaAsignatura = (
  id: string | undefined
): useProgramaAsignaturaType => {
  const [programaAsignatura, setProgramaAsignatura] =
    useState<ProgramaAsignatura | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<boolean>(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getProgramaAsignatura(id)
        setProgramaAsignatura(response)
        setLoading(false)
      } catch (err) {
        console.error(err)
        setError(true)
      }
    }
    fetchData()
  }, [id])

  return { programaAsignatura, setProgramaAsignatura, loading, error }
}

export default useProgramaAsignatura
