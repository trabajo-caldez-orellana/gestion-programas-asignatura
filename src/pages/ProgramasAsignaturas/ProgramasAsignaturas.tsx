import Table from '../../components/Table/Table'
import { useNavigate } from 'react-router-dom'
import './ProgramasAsignaturas.css'
import useProgramasAsignaturas from './hooks/useProgramasAsignaturas'

export default function ProgramasAsignaturas() {
  const navigate = useNavigate()
  const { programasAsignaturas, loading, error } =
    useProgramasAsignaturas()

  const tableColumns = [
    'Carrera',
    'Asignatura',
    'Estado',
    'Programa',
    'Acciones',
  ]


  const verPrograma = (id: number, modoPrograma: string) => {
    navigate(`/programa-asignaturas/${id}`, {state: {modo: modoPrograma} })
  }

  if (error) return <h1>Error</h1>;
  
  if (loading || !programasAsignaturas) return <h1>Cargando...</h1>;

  return (
    <section className="section-content">
      <Table tableColumns={tableColumns} tableData={programasAsignaturas} verPrograma={verPrograma} />
    </section>
  )
}
