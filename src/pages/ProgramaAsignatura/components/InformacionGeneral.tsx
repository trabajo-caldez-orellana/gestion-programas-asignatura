import React from 'react'

import { Titulo, TituloSeccion } from '../../../components'
import { ProgramaAsignaturaInterface } from '../../../interfaces/interfaces'
import { SeccionFormulario } from './SeccionFormulario'

interface InformacionGeneralProps {
  programaAsignatura: ProgramaAsignaturaInterface
}

const InformacionGeneral: React.FC<InformacionGeneralProps> = ({
  programaAsignatura
}) => {
  return (
    <SeccionFormulario>
      <Titulo> NOMBRE DE LA ASIGNATURA</Titulo>
    </SeccionFormulario>
  )
}

export default InformacionGeneral
