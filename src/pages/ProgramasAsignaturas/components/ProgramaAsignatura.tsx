import { useParams, useLocation } from 'react-router-dom'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'
import { ProgramaAsignatura } from '../../../interfaces'
import useProgramaAsignatura from '../hooks/useProgramaAsignatura'
import useProgramaAsignaturaMutation from '../hooks/useProgramaAsignaturaMutation'
import Button from '../../../components/ui/Button'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../../constants/constants'

export default function ProgramaAsignatura() {
  const { id } = useParams()
  const location = useLocation()

  const {
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    loading,
    error
  } = useProgramaAsignatura(id?.toString(), location?.state?.modo)

  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER

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
      <h1>Programa Asignatura</h1>
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

      {errorPostProgramaAsignatura && (
        <p>Error al guardar el programa asignatura</p>
      )}
      {resultPostProgramaAsignatura && <p>Programa enviado correctamente</p>}

      {!modoLectura && (
        <div className="acciones-programa-asignatura">
          <Button text="Guardar borrador" onClick={handlePostPrograma(true)} />
          <Button
            text="Enviar para aprobacion"
            onClick={handlePostPrograma(false)}
          />
        </div>
      )}
    </section>
  )
}
