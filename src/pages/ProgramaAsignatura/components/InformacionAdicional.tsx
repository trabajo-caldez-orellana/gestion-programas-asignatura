import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores
} from '../../../interfaces/interfaces'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  CAMPOS_INFORMACION_ADICIONAL
} from '../../../constants/constants'
import { TituloSeccion } from '../../../components'
import { SeccionFormulario } from './SeccionFormulario'

interface InformacionAdicionalProps {
  programaAsignatura: ProgramaAsignaturaInterface
  setProgramaAsignatura: (
    programaAsignatura: ProgramaAsignaturaInterface
  ) => void
  modoProgramaAsignatura: string
  erroresInfornacionAdicional: ProgramaAsignaturaErrores
}

export default function InformacionAdicional({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura,
  erroresInfornacionAdicional
}: InformacionAdicionalProps) {
  const { informacionAdicional } = programaAsignatura
  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = e.target

    setProgramaAsignatura({
      ...programaAsignatura,
      informacionAdicional: {
        ...programaAsignatura.informacionAdicional,
        [name]: value
      }
    })
  }

  // Los campos se obtienen desde la constante CAMPOS_INFORMACION_ADICIONAL
  return (
    <SeccionFormulario>
      <TituloSeccion>Informacion Adicional</TituloSeccion>
      <form className="informacion-adicional-form">
        {CAMPOS_INFORMACION_ADICIONAL.map((config) => (
          <label htmlFor={config.id} key={config.id}>
            {config.label}
            <textarea
              id={config.id}
              name={config.name}
              value={informacionAdicional[config.name]}
              onChange={handleChange}
              rows={4}
              cols={50}
              disabled={modoLectura}
            />
            {erroresInfornacionAdicional.informacionAdicional[config.name] && (
              <span className="mensaje-error">
                {erroresInfornacionAdicional.informacionAdicional[config.name]}
              </span>
            )}
          </label>
        ))}
      </form>
    </SeccionFormulario>
  )
}
