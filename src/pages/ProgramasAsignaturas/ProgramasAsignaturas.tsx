import Table from '../../components/Table/Table'
import { useNavigate } from 'react-router-dom'
import './ProgramasAsignaturas.css'
import useProgramasAsignaturas from './hooks/useProgramasAsignaturas'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'

export default function ProgramasAsignaturas() {
  const navigate = useNavigate()
  const { programasAsignaturas, loading, error } = useProgramasAsignaturas()

  const tableColumns = [
    'Carrera',
    'Asignatura',
    'Estado',
    'Programa',
    'Acciones'
  ]

  const verPrograma = (id: number | string, modoPrograma: string) => {
    const rutaBase = `/programa-asignaturas`

    switch (modoPrograma) {
      case MODOS_PROGRAMA_ASIGNATURA.VER:
        navigate(`${rutaBase}/${id}`)
        break
      case MODOS_PROGRAMA_ASIGNATURA.EDITAR:
        navigate(`${rutaBase}/editar/${id}`)
        break
      case MODOS_PROGRAMA_ASIGNATURA.NUEVO:
        navigate(`${rutaBase}/nuevo/${id}`)
        break
      default:
    }
  }

  if (error) return <h1>Error</h1>

  if (loading || !programasAsignaturas) return <h1>Cargando...</h1>

  return (
    <section className="section-content">
      <Table
        tableColumns={tableColumns}
        tableData={programasAsignaturas}
        verPrograma={verPrograma}
      />
    </section>
  )
}
