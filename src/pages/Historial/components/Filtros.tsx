import '../Historial.css'
import Button from '../../../components/ui/Button'

export default function Filtros() {
  return (
    <section>
      <section id="filter-container">
        <div className="filter-group">
          <label htmlFor="carrera">Carrera:</label>
          <select id="carrera">
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
          </select>

          <label className="semestre">Semestre:</label>
          <select id="semestre">
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="asignatura">Asignatura:</label>
          <select id="asignatura">
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
          </select>

          <label htmlFor="anio-academico">Año Académico:</label>
          <select id="anio-academico">
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
          </select>
        </div>
      </section>
      <Button text="Buscar" />
    </section>
  )
}
