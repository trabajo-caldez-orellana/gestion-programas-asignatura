import useProgramasVigentes from './hooks/useProgramasVigentes'
import TableProgramasVigentes from './components/TableProgramasVigentes'
import { useNavigate } from 'react-router-dom'

export default function ProgramasVigentes() {
  const navigate = useNavigate()

  const { programasVigentes, loading, error } = useProgramasVigentes()

  const tableColumns = ['Asignatura', 'Estado', 'Acciones']

  if (error) return <h1>Error</h1>

  if (loading || !programasVigentes) return <h1>Cargando...</h1>

  console.log(programasVigentes)

  const verPrograma = (id: number | string, modoPrograma: string) => {
    navigate(`/programa-asignaturas/${id}`, { state: { modo: modoPrograma } })
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
