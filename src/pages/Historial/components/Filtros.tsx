import '../Historial.css'
import Button from '../../../components/ui/Button'
import { Filtros, selectedFiltrosType } from 'types'

interface FiltrosProps {
  filtros: Filtros
  selectedFiltros: selectedFiltrosType | null
  setSelectedFiltros: React.Dispatch<
    React.SetStateAction<selectedFiltrosType | null>
  >
  searchHistorialProgramas: (selectedFiltros: selectedFiltrosType | null) => void
}

export default function Filtros({
  searchHistorialProgramas,
  selectedFiltros,
  filtros,
  setSelectedFiltros
}: FiltrosProps) {
  const handleChangeSelect = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const { id, value } = event.target
    setSelectedFiltros((prevSelectedFiltros) => ({
      ...prevSelectedFiltros!,
      [id]: parseInt(value, 10)
    }))
  }

  return (
    <section id="filter-components-container">
      <section id="filter-container">
        {filtros.map((filtroGroup, index) => (
          <div className="filter-group" key={index}>
            <label htmlFor={filtroGroup.tipo}>{filtroGroup.nombre}:</label>
            <select id={filtroGroup.tipo} onChange={handleChangeSelect}>
              {filtroGroup.opciones.map((opcion) => (
                <option key={opcion.id} value={opcion.id}>
                  {opcion.nombre}
                </option>
              ))}
            </select>
          </div>
        ))}
      </section>
      <Button text="Buscar" onClick={() => searchHistorialProgramas(selectedFiltros)} />
    </section>
  )
}
