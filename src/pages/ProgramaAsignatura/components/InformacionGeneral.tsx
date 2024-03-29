import React from 'react'

import { Formulario, Input, ListadoDatos, Titulo } from '../../../components'
import { ProgramaAsignaturaInterface } from '../../../interfaces/interfaces'
import { SeccionFormulario, InputOutsideContainer } from './SeccionFormulario'

interface InformacionGeneralProps {
  programaAsignatura: ProgramaAsignaturaInterface
}

const InformacionGeneral: React.FC<InformacionGeneralProps> = ({
  programaAsignatura
}) => {
  const { informacionGeneral } = programaAsignatura

  return (
    <SeccionFormulario>
      <Titulo> {informacionGeneral.nombreAsignatura.toUpperCase()}</Titulo>
      <Formulario>
        <Input
          id="codigo"
          name="codigo"
          onChange={() => {}}
          value={informacionGeneral.codigoAsignatura}
          mensajeDeError=""
          label="Codigo"
          type="text"
          modoLectura
        />
        <Input
          id="anio"
          name="anio"
          onChange={() => {}}
          value={informacionGeneral.anioAcademico}
          mensajeDeError=""
          label="Año Académico"
          type="text"
          modoLectura
        />
        <Input
          id="bloque"
          name="bloque"
          onChange={() => {}}
          value={informacionGeneral.bloqueCurricular}
          mensajeDeError=""
          label="Bloque de Conocimiento"
          type="text"
          modoLectura
        />

        <InputOutsideContainer>
          <ListadoDatos
            datos={informacionGeneral.carreras}
            tituloListado="Carrera/s"
          />
        </InputOutsideContainer>
        <InputOutsideContainer>
          <ListadoDatos
            datos={informacionGeneral.equipoDocente}
            tituloListado="Equipo docente"
          />
        </InputOutsideContainer>
      </Formulario>
    </SeccionFormulario>
  )
}

export default InformacionGeneral
