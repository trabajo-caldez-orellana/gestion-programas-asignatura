import Table from '../../components/Table/Table'
import { useNavigate } from 'react-router-dom'
import './ProgramasAsignaturas.css'

export default function ProgramasAsignaturas() {
  const navigate = useNavigate()
  const tableColumns = [
    'Carrera',
    'Asignatura',
    'Ultima version',
    'Estado',
    'Acciones'
  ]

  const tableData = [
    { id: 1, carrera: 'Item 1', version: 'Item 1', estado: 'Item 1' },
    { id: 2, carrera: 'Item 2', version: 'Item 2', estado: 'Item 2' },
    { id: 3, carrera: 'Item 3', version: 'Item 3', estado: 'Item 3' }
  ]

  const watch = (id: number) => {
    navigate(`/programa-asignaturas/${id}`)
  }

  return (
    <section className="section-content">
      <Table tableColumns={tableColumns} tableData={tableData} watch={watch} />
    </section>
  )
}
