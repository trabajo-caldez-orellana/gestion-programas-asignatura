import { useState } from 'react'
import useHistorial from './hooks/useHistorial'
import useFiltros from './hooks/useFiltros'
import TableHistorial from './components/TableHistorial'
import { useNavigate } from 'react-router-dom'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'
import Filtros from './components/Filtros'
import { ProgramasHistorial } from '../../types'
import { client } from '../../utils/axiosClient'


export default function Historial() {
  const navigate = useNavigate()
  const [programasHistorial, setProgramasHistorial] =
    useState<ProgramasHistorial | null>(null)

  const {
    filtros,
    selectedFiltros,
    setSelectedFiltros,
    loadingFiltros,
    errorFiltros
  } = useFiltros()

  const { searchHistorialProgramas, loading, error } = useHistorial({ setProgramasHistorial })

  const tableColumns = ['Asignatura', 'Acciones']

  if (error || errorFiltros) return <h1>Error</h1>

  if (loading || loadingFiltros || !filtros)
    return <h1>Cargando...</h1>

  const verPrograma = (id: number | null, modoPrograma: string) => {
    if (modoPrograma === MODOS_PROGRAMA_ASIGNATURA.VER)
      navigate(`/programa-asignaturas/${id}`)
  }

  const imprimir = (id: number | string | null) => {
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
      <Filtros
        filtros={filtros}
        setSelectedFiltros={setSelectedFiltros}
        searchHistorialProgramas={searchHistorialProgramas}
        selectedFiltros={selectedFiltros}
      />
      <TableHistorial
        tableColumns={tableColumns}
        tableData={programasHistorial}
        verPrograma={verPrograma}
        imprimir={imprimir}
      />
    </section>
  )
}
