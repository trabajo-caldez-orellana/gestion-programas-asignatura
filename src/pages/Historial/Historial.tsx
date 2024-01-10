import useHistorial from './hooks/useHistorial'
import TableHistorial from './components/TableHistorial'
import { useNavigate } from 'react-router-dom'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import Filtros from './components/Filtros'

export default function Historial() {
  const navigate = useNavigate()

  const { programasVigentes, loading, error } = useHistorial()

  const tableColumns = ['Asignatura', 'Estado', 'Acciones']

  if (error) return <h1>Error</h1>

  if (loading || !programasVigentes) return <h1>Cargando...</h1>

  console.log(programasVigentes)

  const verPrograma = (id: number | null, modoPrograma: string) => {
    if (modoPrograma === MODOS_PROGRAMA_ASIGNATURA.VER)
      navigate(`/programa-asignaturas/${id}`)
  }

  return (
    <section className="section-content">
      <Filtros />
      <TableHistorial
        tableColumns={tableColumns}
        tableData={programasVigentes}
        verPrograma={verPrograma}
      />
    </section>
  )
}
