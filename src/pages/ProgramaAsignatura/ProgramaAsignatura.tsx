import { useParams } from 'react-router-dom'

import {
  CargaHoraria,
  InformacionAdicional,
  SeccionDescriptores,
  BotonesProgramaAsignatura
} from './components'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import useProgramaAsignatura from './hooks/useProgramaAsignatura'
import './ProgramaAsignatura.css'

const ProgramaAsignatura: React.FC<{ modo: string }> = ({ modo }) => {
  // EN el caso de ser modo = NUEVO o EDITAR_ULTIMO, este id corresponderia a la asignatura a la que estamos entrando!!
  const { id } = useParams()

  // Este hook se encarga de hacer el get del programaAsignatura
  const {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    loading,
    error,
    mensajeDeError,
    erroresProgramaAsignatura,
    guardarPrograma
  } = useProgramaAsignatura(id?.toString(), modo)

  const modoLectura = modo === MODOS_PROGRAMA_ASIGNATURA.VER
  const handlePostPrograma = (presentar: boolean) => () => {
    guardarPrograma(presentar)
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
      <CargaHoraria programaAsignatura={programaAsignatura} />
      <SeccionDescriptores
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
        modoProgramaAsignatura={modoProgramaAsignatura}
        erroresPrograma={erroresProgramaAsignatura}
      />
      <InformacionAdicional
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
        modoProgramaAsignatura={modoProgramaAsignatura}
        erroresInfornacionAdicional={erroresProgramaAsignatura}
      />
      <br />
      <BotonesProgramaAsignatura
        error={erroresProgramaAsignatura.all}
        modoLectura={modoLectura}
        handlePostPrograma={handlePostPrograma}
      />
    </section>
  )
}

export default ProgramaAsignatura
