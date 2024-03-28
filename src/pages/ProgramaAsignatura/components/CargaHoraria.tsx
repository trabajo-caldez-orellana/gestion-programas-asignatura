import { ProgramaAsignaturaInterface } from '../../../interfaces'
import camelCase from 'lodash/camelCase'
import { CAMPOS_CARGA_HORARIA } from '../../../constants/constants'
import { Formulario, TituloSeccion, Input } from '../../../components'
import { SeccionFormulario, InputOutsideContainer } from './SeccionFormulario'

interface CargaHorariaProps {
  programaAsignatura: ProgramaAsignaturaInterface
}

export default function CargaHoraria({
  programaAsignatura
}: CargaHorariaProps) {
  const { cargaHoraria } = programaAsignatura

  // Los campos se obtienen desde la constante CAMPOS_CARGA_HORARIA
  return (
    <SeccionFormulario>
      <TituloSeccion>CARGA HORARIA</TituloSeccion>
      <Formulario>
        {CAMPOS_CARGA_HORARIA.map((config) => {
          if (cargaHoraria[camelCase(config.name)]) {
            return (
              <InputOutsideContainer key={config.id}>
                <Input
                  id={config.id}
                  name={config.name}
                  onChange={() => {}}
                  value={cargaHoraria[camelCase(config.name)] || 0}
                  mensajeDeError=""
                  label={config.label}
                  type="number"
                  modoLectura
                />
              </InputOutsideContainer>
            )
          }

          return null
        })}
      </Formulario>
    </SeccionFormulario>
  )
}
