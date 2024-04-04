import useProgramasVigentes from './hooks/useProgramasVigentes'
import TableProgramasVigentes from './components/TableProgramasVigentes'
import { useNavigate } from 'react-router-dom'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import { client } from '../../utils/axiosClient'
import { RUTAS_PAGINAS } from '../../constants/constants'

export default function ProgramasVigentes() {
  const navigate = useNavigate()

  const { programasVigentes, loading, error } = useProgramasVigentes()

  const tableColumns = ['Asignatura', 'Estado', 'Acciones']

  if (error) return <h1>Error</h1>

  if (loading || !programasVigentes) return <h1>Cargando...</h1>

  const verPrograma = (id: number | string, modoPrograma: string) => {
    if (modoPrograma === MODOS_PROGRAMA_ASIGNATURA.VER)
      navigate(`${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${id}`)
  }

  const imprimir = (id: number | string) => {
    const descargarPDF = async () => {
      try {
        const response = await client.get(`/api/programas/pdf/${id}/`, {
          responseType: 'blob'
        })

        // Crear un objeto URL a partir de los datos recibidos
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)

        // Crear un enlace <a> y simular clic para descargar el archivo
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'programa.pdf')
        document.body.appendChild(link)
        link.click()

        // Liberar el objeto URL
        window.URL.revokeObjectURL(url)
      } catch (error) {
        console.error('Error al descargar el PDF:', error)
      }
    }

    descargarPDF()
  }

  return (
    <section className="section-content">
      <TableProgramasVigentes
        tableColumns={tableColumns}
        tableData={programasVigentes}
        verPrograma={verPrograma}
        imprimir={imprimir}
      />
    </section>
  )
}
