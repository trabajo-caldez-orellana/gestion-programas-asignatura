import { camelCase } from 'lodash'
import { ProgramaAsignaturaInterface } from '../../../interfaces'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  CAMPOS_INFORMACION_ADICIONAL
} from '../../../constants/constants'

interface InformacionAdicionalProps {
  programaAsignatura: ProgramaAsignaturaInterface
  setProgramaAsignatura: (
    programaAsignatura: ProgramaAsignaturaInterface
  ) => void
  modoProgramaAsignatura: string
}

export default function InformacionAdicional({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura
}: InformacionAdicionalProps) {
  const { informacionAdicional } = programaAsignatura
  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = e.target

    setProgramaAsignatura({
      ...programaAsignatura,
      informacionAdicional: {
        ...programaAsignatura.informacionAdicional,
        [camelCase(name)]: value
      }
    })
  }

  // Los campos se obtienen desde la constante CAMPOS_INFORMACION_ADICIONAL
  return (
    <section className="form-section">
      <h2 className="header">Informacion Adicional</h2>
      <form className="informacion-adicional-form">
        {CAMPOS_INFORMACION_ADICIONAL.map((config) => (
          <label htmlFor={config.id} key={config.id}>
            {config.label}
            <textarea
              id={config.id}
              name={config.name}
              value={informacionAdicional[camelCase(config.name)]}
              onChange={handleChange}
              rows={4}
              cols={50}
              disabled={modoLectura}
            />
          </label>
        ))}
      </form>
    </section>
  )
}
