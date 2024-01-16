import { ProgramaAsignatura } from '../../../interfaces'
import camelCase from 'lodash/camelCase'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  CAMPOS_CARGA_HORARIA
} from '../../../constants/constants'

interface CargaHorariaProps {
  programaAsignatura: ProgramaAsignatura
  setProgramaAsignatura: (programaAsignatura: ProgramaAsignatura) => void
  modoProgramaAsignatura: string
}

export default function CargaHoraria({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura
}: CargaHorariaProps) {
  const { cargaHoraria } = programaAsignatura
  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER

  const handleCargaHorariaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target

    setProgramaAsignatura({
      ...programaAsignatura,
      cargaHoraria: {
        ...programaAsignatura.cargaHoraria,
        [camelCase(name)]: value
      }
    })
  }

  // Los campos se obtienen desde la constante CAMPOS_CARGA_HORARIA
  return (
    <section className="form-section">
      <h2 className="header">Carga Horaria</h2>
      <form className="carga-horaria-form">
        {CAMPOS_CARGA_HORARIA.map((config) => (
          <>
            <label htmlFor={config.id}>{config.label}</label>
            <input
              type="text"
              id={config.id}
              name={config.name}
              value={cargaHoraria[camelCase(config.name)]}
              onChange={handleCargaHorariaChange}
              disabled={modoLectura}
            />
          </>
        ))}
      </form>
    </section>
  )
}
