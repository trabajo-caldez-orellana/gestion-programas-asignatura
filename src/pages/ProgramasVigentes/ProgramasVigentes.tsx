import useProgramasVigentes from './hooks/useProgramasVigentes'
import TableProgramasVigentes from './components/TableProgramasVigentes'
import { useNavigate } from 'react-router-dom'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'

export default function ProgramasVigentes() {
  const navigate = useNavigate()

  const { programasVigentes, loading, error } = useProgramasVigentes()

  const tableColumns = ['Asignatura', 'Estado', 'Acciones']

  if (error) return <h1>Error</h1>

  if (loading || !programasVigentes) return <h1>Cargando...</h1>

  const verPrograma = (id: number | string, modoPrograma: string) => {
    if (modoPrograma === MODOS_PROGRAMA_ASIGNATURA.VER)
      navigate(`/programa-asignaturas/${id}`)
  }
  return (
    <section className="section-content">
      <TableProgramasVigentes
        tableColumns={tableColumns}
        tableData={programasVigentes}
        verPrograma={verPrograma}
      />
    </section>
  )
}
