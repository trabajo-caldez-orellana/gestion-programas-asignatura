import { ProgramaAsignaturaInterface } from '../../../interfaces'
import camelCase from 'lodash/camelCase'
import { CAMPOS_CARGA_HORARIA } from '../../../constants/constants'

interface CargaHorariaProps {
  programaAsignatura: ProgramaAsignaturaInterface
}

export default function CargaHoraria({
  programaAsignatura
}: CargaHorariaProps) {
  const { cargaHoraria } = programaAsignatura

  // Los campos se obtienen desde la constante CAMPOS_CARGA_HORARIA
  return (
    <section className="form-section">
      <h2 className="header">Carga Horaria</h2>
      <form className="carga-horaria-form">
        {CAMPOS_CARGA_HORARIA.map((config) => (
          <label htmlFor={config.id} key={config.id}>
            {config.label}
            <input
              type="text"
              id={config.id}
              name={config.name}
              value={cargaHoraria[camelCase(config.name)]}
              disabled={true}
            />
          </label>
        ))}
      </form>
    </section>
  )
}
