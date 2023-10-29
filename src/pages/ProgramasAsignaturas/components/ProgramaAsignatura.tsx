import { useParams } from 'react-router-dom'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'
import { ProgramaAsignatura } from '../../../interfaces'
import useProgramaAsignatura from '../hooks/useProgramaAsignatura'

export default function ProgramaAsignatura() {
  const { id } = useParams()

  const { programaAsignatura, setProgramaAsignatura, loading, error } =
    useProgramaAsignatura(id?.toString())

  if (error) return <h1>Error</h1>;
  
  if (loading || !programaAsignatura) return <h1>Cargando...</h1>;

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
    </section>
  )
}
