import { ProgramaAsignaturaInterface } from '../../../interfaces'
import camelCase from 'lodash/camelCase'
import { CAMPOS_CARGA_HORARIA } from '../../../constants/constants'
import { Formulario, TituloSeccion, Input } from '../../../components'
import { SeccionFormulario } from './SeccionFormulario'

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
          console.log(config.name, cargaHoraria[config.name])
          if (cargaHoraria[camelCase(config.name)]) {
            return (
              <Input
                id={config.id}
                key={config.id}
                name={config.name}
                onChange={() => {}}
                value={cargaHoraria[camelCase(config.name)]}
                mensajeDeError=""
                label={config.label}
                type="number"
                modoLectura
              />
            )
          }

          return null
        })}
      </Formulario>
    </SeccionFormulario>
  )
}
