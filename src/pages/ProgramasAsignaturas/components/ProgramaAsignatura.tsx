// import { useParams } from 'react-router-dom'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'

export default function ProgramaAsignatura() {
  //const { id } = useParams()
  return (
    <section className="section-content">
      <h1>ProgramaAsignatura</h1>
      <CargaHoraria />
      <SeccionDescriptores />
      <InformacionAdicional />
    </section>
  )
}
