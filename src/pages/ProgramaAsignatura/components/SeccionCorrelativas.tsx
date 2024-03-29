import React from 'react'

import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores,
  Correlativa
} from '../../../interfaces/interfaces'
import {
  TIPO_CORRELATIVA,
  REQUISITOS_CORRELATIVA,
  DatoListaInterface,
  MODOS_PROGRAMA_ASIGNATURA
} from '../../../constants/constants'
import { SeccionFormulario } from './SeccionFormulario'
import { TituloSeccion } from '../../../components'
import {
  CorrelativaAsignaturas,
  CorrelativaCantidad
} from './ObjetosListaCorrelativas'

const ASIGNATURAS_DISPONIBLES_EJEMPLO: DatoListaInterface[] = [
  {
    id: 1,
    informacion: 'Calculo I'
  },
  {
    id: 2,
    informacion: 'Calculo II'
  },
  {
    id: 3,
    informacion: 'Calculo III'
  },
  {
    id: 4,
    informacion: 'Algebra I'
  },
  {
    id: 1,
    informacion: 'Algebra II'
  }
]

interface SeccionCorrelativasProps {
  programaAsignatura: ProgramaAsignaturaInterface
  setProgramaAsignatura: (
    programaAsignatura: ProgramaAsignaturaInterface
  ) => void
  modoProgramaAsignatura: string
  erroresSeccionCorrelativas: ProgramaAsignaturaErrores
}

const SeccionCorrelativas: React.FC<SeccionCorrelativasProps> = ({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura,
  erroresSeccionCorrelativas
}) => {
  console.log(
    programaAsignatura,
    setProgramaAsignatura,
    modoProgramaAsignatura,
    erroresSeccionCorrelativas
  )

  const modoLectura =
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER ||
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.REVISAR

  const OBJETO_PRUEBA_CORRELATIVAS: Correlativa[] = [
    {
      id: 1,
      tipo: TIPO_CORRELATIVA.REGULAR,
      requisito: REQUISITOS_CORRELATIVA.ASIGNATURA,
      asignatura: ASIGNATURAS_DISPONIBLES_EJEMPLO[0]
    },
    {
      id: 2,
      tipo: TIPO_CORRELATIVA.REGULAR,
      requisito: REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS,
      cantidadAsignaturas: 20
    },
    {
      id: 3,
      tipo: TIPO_CORRELATIVA.REGULAR,
      requisito: REQUISITOS_CORRELATIVA.MODULO,
      modulo: 'II'
    },
    {
      id: 4,
      tipo: TIPO_CORRELATIVA.APROBADO,
      requisito: REQUISITOS_CORRELATIVA.ASIGNATURA,
      asignatura: ASIGNATURAS_DISPONIBLES_EJEMPLO[1]
    },
    {
      id: 5,
      tipo: TIPO_CORRELATIVA.APROBADO,
      requisito: REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS,
      cantidadAsignaturas: 20
    },
    {
      id: 6,
      tipo: TIPO_CORRELATIVA.APROBADO,
      requisito: REQUISITOS_CORRELATIVA.MODULO,
      modulo: 'I'
    }
  ]

  const handleSeleccionarCorrelativaAsignatura = (
    indice: number,
    asignaturaSeleccionada: number | string
  ) => {
    console.log('Modificar numero ', indice, ' de la lista')
    console.log('Asignatura seleccionada: ', asignaturaSeleccionada)
  }

  const handleBorrarCorrelativa = (indice: number) => {
    console.log('Eliminando Correlativa', indice)
  }

  const enCambioTipoCorrelativa = (
    indice: number,
    tipoCorrelativa: TIPO_CORRELATIVA
  ) => {
    console.log(
      'Cambiando la correlativa a correlativa numero ',
      indice,
      tipoCorrelativa
    )
  }

  return (
    <SeccionFormulario>
      <TituloSeccion>CORRELATIVAS</TituloSeccion>
      {OBJETO_PRUEBA_CORRELATIVAS.map((correlativa, index) => {
        if (
          correlativa.requisito === REQUISITOS_CORRELATIVA.ASIGNATURA &&
          !!correlativa.asignatura
        ) {
          return (
            <CorrelativaAsignaturas
              modoLectura={modoLectura}
              key={`${programaAsignatura.id}${index}`}
              tipo={correlativa.tipo}
              asignaturasDisponibles={ASIGNATURAS_DISPONIBLES_EJEMPLO}
              asignaturaSeleccionada={correlativa.asignatura.id}
              enCambioAsignaturaSeleccionada={(seleccion: number | string) =>
                handleSeleccionarCorrelativaAsignatura(index, seleccion)
              }
              enBorradoCorrelativa={() => handleBorrarCorrelativa(index)}
              enCambioTipoCorrelativa={(seleccion) =>
                enCambioTipoCorrelativa(index, seleccion)
              }
            />
          )
        }

        if (
          correlativa.requisito === REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS
        ) {
          return (
            <CorrelativaCantidad
              cantidadAsignaturas={correlativa.cantidadAsignaturas || 0}
              tipo={correlativa.tipo}
              enCambioCantidadAsignaturas={() => {}}
              enBorradoCorrelativa={() => handleBorrarCorrelativa(index)}
              enCambioTipoCorrelativa={(seleccion) =>
                enCambioTipoCorrelativa(index, seleccion)
              }
              modoLectura={modoLectura}
            />
          )
        }

        if (
          correlativa.requisito === REQUISITOS_CORRELATIVA.MODULO &&
          !!correlativa.modulo
        )
          return <></>
      })}
    </SeccionFormulario>
  )
}

export default SeccionCorrelativas
