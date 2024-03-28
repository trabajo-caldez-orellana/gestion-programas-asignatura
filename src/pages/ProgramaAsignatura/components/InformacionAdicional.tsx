import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores
} from '../../../interfaces/interfaces'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  CAMPOS_INFORMACION_ADICIONAL
} from '../../../constants/constants'
import { TituloSeccion, Formulario, TextArea } from '../../../components'
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
  const modoLectura =
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER ||
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.REVISAR

  const handleChange = (name: string, value: string) => {
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
      <Formulario>
        {CAMPOS_INFORMACION_ADICIONAL.map((config) => (
          <TextArea
            key={config.id}
            modoLectura={modoLectura}
            label={config.label}
            name={config.name}
            id={config.name}
            value={informacionAdicional[config.name]}
            onChange={handleChange}
            mensajeDeError={
              erroresInfornacionAdicional.informacionAdicional[config.name]
            }
          />
        ))}
      </Formulario>
    </SeccionFormulario>
  )
}
