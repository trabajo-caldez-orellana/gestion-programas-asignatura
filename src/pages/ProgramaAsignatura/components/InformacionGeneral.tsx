import React from 'react'

import { Formulario, Input, ListadoDatos, Titulo } from '../../../components'
import { ProgramaAsignaturaInterface } from '../../../interfaces/interfaces'
import { SeccionFormulario, InputOutsideContainer } from './SeccionFormulario'
import { DatoListaInterface } from '../../../constants/constants'

interface InformacionGeneralProps {
  programaAsignatura: ProgramaAsignaturaInterface
}

const INFORMACION_ADICIONAL = {
  nombreAsignatura: 'Calculo II',
  codigoAsignatura: '15_C11',
  anioAcademico: 'Anio Academico 2024',
  bloqueCurricular: 'Ciencias Basicas',
  carreras: [
    { id: 1, nombre: 'Ingenieria en Computacion' },
    { id: 2, nombre: 'Ingenieria Quimica' },
    { id: 3, nombre: 'Ingenieria Informatica' }
  ],
  asignaturasCorrelativas: [
    {
      id: 1,
      nombre: 'Calculo  I',
      tipo: 'Aprobado'
    },
    {
      id: 2,
      nombre: 'Calculo  II',
      tipo: 'Regular'
    }
  ],
  equipoDocente: [
    {
      id: 1,
      nombre: 'Esteban Volentini',
      cargo: 'Titular Docente',
      dedicacion: 'Exclusiva'
    },
    {
      id: 2,
      nombre: 'Esteban Volentini',
      cargo: 'Titular Docente',
      dedicacion: 'Exclusiva'
    },
    {
      id: 3,
      nombre: 'Esteban Volentini',
      cargo: 'Titular Docente',
      dedicacion: 'Exclusiva'
    }
  ]
}

const InformacionGeneral: React.FC<InformacionGeneralProps> = ({
  programaAsignatura
}) => {
  console.log('progamaAsignatura pa q no se queje', programaAsignatura)

  const datosDocentes: DatoListaInterface[] =
    INFORMACION_ADICIONAL.equipoDocente.map((docente) => {
      return {
        id: docente.id,
        informacion: `${docente.nombre} - ${docente.cargo} - ${docente.dedicacion}`
      }
    })

  const datosCorrelativas: DatoListaInterface[] =
    INFORMACION_ADICIONAL.asignaturasCorrelativas.map((asignatura) => {
      return {
        id: asignatura.id,
        informacion: `${asignatura.nombre} - ${asignatura.tipo}`
      }
    })
  const datosCarreras: DatoListaInterface[] =
    INFORMACION_ADICIONAL.asignaturasCorrelativas.map((carrera) => {
      return {
        id: carrera.id,
        informacion: carrera.nombre
      }
    })

  return (
    <SeccionFormulario>
      <Titulo> {INFORMACION_ADICIONAL.nombreAsignatura.toUpperCase()}</Titulo>
      <Formulario>
        <Input
          id="codigo"
          name="codigo"
          onChange={() => {}}
          value={INFORMACION_ADICIONAL.codigoAsignatura}
          mensajeDeError=""
          label="Codigo"
          type="text"
          modoLectura
        />
        <Input
          id="anio"
          name="anio"
          onChange={() => {}}
          value={INFORMACION_ADICIONAL.anioAcademico}
          mensajeDeError=""
          label="Año Académico"
          type="text"
          modoLectura
        />
        <Input
          id="bloque"
          name="bloque"
          onChange={() => {}}
          value={INFORMACION_ADICIONAL.bloqueCurricular}
          mensajeDeError=""
          label="Bloque de Conocimiento"
          type="text"
          modoLectura
        />

        <InputOutsideContainer>
          <ListadoDatos datos={datosCarreras} tituloListado="Carrera/s" />
        </InputOutsideContainer>
        <InputOutsideContainer>
          <ListadoDatos datos={datosDocentes} tituloListado="Equipo docente" />
        </InputOutsideContainer>
        <InputOutsideContainer>
          <ListadoDatos
            datos={datosCorrelativas}
            tituloListado="Correlativas"
          />
        </InputOutsideContainer>
      </Formulario>
    </SeccionFormulario>
  )
}

export default InformacionGeneral
