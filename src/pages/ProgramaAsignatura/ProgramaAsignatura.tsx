import { useState } from 'react'
import { useParams } from 'react-router-dom'

import {
  CargaHoraria,
  InformacionAdicional,
  SeccionDescriptores,
  BotonesProgramaAsignatura,
  BotonesRevisionProgramaAsignatura
} from './components'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import useProgramaAsignatura from './hooks/useProgramaAsignatura'
import './ProgramaAsignatura.css'

const ProgramaAsignatura: React.FC<{ modo: string }> = ({ modo }) => {
  // EN el caso de ser modo = NUEVO o EDITAR_ULTIMO, este id corresponderia a la asignatura a la que estamos entrando!!
  const { id } = useParams()
  const [erroresCorreccion, setErroresCorreccion] = useState<string>('')

  // Este hook se encarga de hacer el get del programaAsignatura
  const {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    loading,
    errorInesperado,
    erroresProgramaAsignatura,
    guardarPrograma
  } = useProgramaAsignatura(id?.toString(), modo)

  const modoLectura =
    modo === MODOS_PROGRAMA_ASIGNATURA.VER ||
    modo === MODOS_PROGRAMA_ASIGNATURA.REVISAR

  const handlePostPrograma = (presentar: boolean) => () => {
    // TODO. Hacer validaciones en el frontend para que no se manden
    // formularios que sean no validos!
    guardarPrograma(presentar)
  }

  const handleAprobarPrograma = () => {
    console.log('Aprobar programa')
    setErroresCorreccion('')
  }

  const handlePedirCambiosPrograma = (mensaje: string) => {
    console.log('Pedir cambios: ', mensaje)
    setErroresCorreccion('')
  }

  if (errorInesperado)
    return (
      <div>
        <h1>Error</h1>
        <p>{errorInesperado}</p>
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
      {modo === MODOS_PROGRAMA_ASIGNATURA.REVISAR ? (
        <BotonesRevisionProgramaAsignatura
          handleAprobarPrograma={handleAprobarPrograma}
          handlePedirCambiosPrograma={handlePedirCambiosPrograma}
          error={erroresCorreccion}
        />
      ) : (
        <BotonesProgramaAsignatura
          error={erroresProgramaAsignatura.all}
          modoLectura={modoLectura}
          handlePostPrograma={handlePostPrograma}
        />
      )}
    </section>
  )
}

export default ProgramaAsignatura
