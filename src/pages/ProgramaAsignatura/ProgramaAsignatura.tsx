import { useParams } from 'react-router-dom'

import {
  CargaHoraria,
  InformacionAdicional,
  SeccionDescriptores,
  BotonesProgramaAsignatura,
  BotonesRevisionProgramaAsignatura,
  InformacionGeneral,
  SeccionCorrelativas
} from './components'
import { Spinner } from '../../components'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import useProgramaAsignatura from './hooks/useProgramaAsignatura'

const ProgramaAsignatura: React.FC<{ modo: string }> = ({ modo }) => {
  // EN el caso de ser modo = NUEVO o EDITAR_ULTIMO, este id corresponderia a la asignatura a la que estamos entrando!!
  const { id } = useParams()

  // Este hook se encarga de hacer el get del programaAsignatura
  const {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    cargandoPrograma: loading,
    errorCargandoPrograma: errorInesperado,
    erroresProgramaAsignatura,
    guardarPrograma,
    aprobarPrograma,
    pedirCambiosPrograma,
    asignaturasDisponibles,
    accionEnProgreso
  } = useProgramaAsignatura(id?.toString(), modo)

  const modoLectura =
    modo === MODOS_PROGRAMA_ASIGNATURA.VER ||
    modo === MODOS_PROGRAMA_ASIGNATURA.REVISAR

  const handlePostPrograma = (presentar: boolean) => () => {
    guardarPrograma(presentar)
  }

  const handleAprobarPrograma = () => {
    aprobarPrograma()
  }

  const handlePedirCambiosPrograma = (mensaje: string) => {
    pedirCambiosPrograma(mensaje)
  }

  if (errorInesperado)
    return (
      <div>
        <h1>Error</h1>
        <p>{errorInesperado}</p>
      </div>
    )

  if (loading) return <Spinner />

  return (
    <section className="section-content">
      <InformacionGeneral programaAsignatura={programaAsignatura} />
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
      <SeccionCorrelativas
        asignaturasDisponibles={asignaturasDisponibles}
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
        modoProgramaAsignatura={modoProgramaAsignatura}
        erroresSeccionCorrelativas={erroresProgramaAsignatura}
      />
      <br />
      {modo === MODOS_PROGRAMA_ASIGNATURA.REVISAR ? (
        <BotonesRevisionProgramaAsignatura
          handleAprobarPrograma={handleAprobarPrograma}
          handlePedirCambiosPrograma={handlePedirCambiosPrograma}
          error={erroresProgramaAsignatura.all}
          isLoading={accionEnProgreso}
        />
      ) : (
        <BotonesProgramaAsignatura
          error={erroresProgramaAsignatura.all}
          modoLectura={modoLectura}
          handlePostPrograma={handlePostPrograma}
          isLoading={accionEnProgreso}
        />
      )}
    </section>
  )
}

export default ProgramaAsignatura
