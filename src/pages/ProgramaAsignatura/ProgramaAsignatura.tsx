import { useParams } from 'react-router-dom'

import {
  CargaHoraria,
  InformacionAdicional,
  SeccionDescriptores,
  BotonesProgramaAsignatura
} from './components'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import { ProgramaAsignatura } from '../../interfaces'
import useProgramaAsignatura from './hooks/useProgramaAsignatura'
import useProgramaAsignaturaMutation from './hooks/useProgramaAsignaturaMutation'
import './ProgramaAsignatura.css'

export default function ProgramaAsignatura({ modo }: { modo: string }) {
  const { id } = useParams()

  // Este hook se encarga de hacer el get del programaAsignatura
  const {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    loading,
    error,
    mensajeDeError
  } = useProgramaAsignatura(id?.toString(), modo)

  const modoLectura = modo === MODOS_PROGRAMA_ASIGNATURA.VER

  // Este hook se encarga de hacer el post del programaAsignatura
  const {
    postPrograma,
    resultPostProgramaAsignatura,
    errorPostProgramaAsignatura
  } = useProgramaAsignaturaMutation(programaAsignatura)

  const handlePostPrograma = (isDraft: boolean) => () => {
    postPrograma(isDraft)
  }

  if (error)
    return (
      <div>
        <h1>Error</h1>
        <p>{mensajeDeError}</p>
      </div>
    )

  if (loading || !programaAsignatura) return <h1>Cargando...</h1>

  return (
    <section className="section-content">
      <CargaHoraria
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
        modoProgramaAsignatura={modoProgramaAsignatura}
      />
      <SeccionDescriptores
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
        modoProgramaAsignatura={modoProgramaAsignatura}
      />
      <InformacionAdicional
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
        modoProgramaAsignatura={modoProgramaAsignatura}
      />
      <br />
      <BotonesProgramaAsignatura
        errorPostProgramaAsignatura={errorPostProgramaAsignatura}
        resultPostProgramaAsignatura={resultPostProgramaAsignatura}
        modoLectura={modoLectura}
        handlePostPrograma={handlePostPrograma}
      />
    </section>
  )
}