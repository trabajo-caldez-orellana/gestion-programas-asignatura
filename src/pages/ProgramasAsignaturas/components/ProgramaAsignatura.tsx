import { useParams, useLocation } from 'react-router-dom'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'
import { ProgramaAsignatura } from '../../../interfaces'
import useProgramaAsignatura from '../hooks/useProgramaAsignatura'
import useProgramaAsignaturaMutation from '../hooks/useProgramaAsignaturaMutation'
import BotonesProgramaAsignatura from './BotonesProgramaAsignatura'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../../constants/constants'

export default function ProgramaAsignatura() {
  const { id } = useParams()

  // Con useLocation obtengo el modo que le paso desde ProgramasAsignaturas.tsx
  const location = useLocation()

  // Este hook se encarga de hacer el get del programaAsignatura
  const {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    loading,
    error
  } = useProgramaAsignatura(id?.toString(), location?.state?.modo)

  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER

  // Este hook se encarga de hacer el post del programaAsignatura
  const {
    postPrograma,
    resultPostProgramaAsignatura,
    errorPostProgramaAsignatura
  } = useProgramaAsignaturaMutation(programaAsignatura)

  const handlePostPrograma = (isDraft: boolean) => () => {
    postPrograma(isDraft)
  }

  if (error) return <h1>Error</h1>

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
