import { useState } from 'react'
import { ProgramaAsignatura } from '../../../interfaces'
import { postProgramaAsignatura } from '../services'

type useProgramaAsignaturaMutationType = {
  postPrograma: (isDraft: boolean) => void
  resultPostProgramaAsignatura: boolean
  errorPostProgramaAsignatura: boolean
}

const useProgramaAsignatura = (
  programaAsignatura: ProgramaAsignatura | null
): useProgramaAsignaturaMutationType => {
  const [resultPostProgramaAsignatura, setResultPostProgramaAsignatura] = useState<boolean>(false)
  const [errorPostProgramaAsignatura, setError] = useState<boolean>(false)

  const postPrograma = async (isDraft: boolean) => {
    try {
      const response = await postProgramaAsignatura(programaAsignatura, isDraft)
      setResultPostProgramaAsignatura(response.success)
    } catch (err) {
      console.error(err)
      setError(true)
    }
  }

  return {
    postPrograma,
    resultPostProgramaAsignatura,
    errorPostProgramaAsignatura
  }
}

export default useProgramaAsignatura
