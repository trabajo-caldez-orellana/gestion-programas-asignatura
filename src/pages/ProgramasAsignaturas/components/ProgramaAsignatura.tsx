import { useParams } from 'react-router-dom'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'
import { ProgramaAsignatura } from '../../../interfaces'
import useProgramaAsignatura from '../hooks/useProgramaAsignatura'
import useProgramaAsignaturaMutation from '../hooks/useProgramaAsignaturaMutation'
import Button from '../../../components/ui/Button'

export default function ProgramaAsignatura() {
  const { id } = useParams()

  const { programaAsignatura, setProgramaAsignatura, loading, error } =
    useProgramaAsignatura(id?.toString())

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
      />
      <SeccionDescriptores
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
      />
      <InformacionAdicional
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
      />

      {
        errorPostProgramaAsignatura && (
          <p>Error al guardar el programa asignatura</p>
        )
      }
      {
        resultPostProgramaAsignatura && (
          <p>Programa enviado correctamente</p>
        )
      }

      <div className="acciones-programa-asignatura">
        <Button text="Guardar borrador" onClick={handlePostPrograma(true)} />
        <Button
          text="Enviar para aprobacion"
          onClick={handlePostPrograma(false)}
        />
      </div>
    </section>
  )
}
