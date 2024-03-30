import React, { useState } from 'react'

import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores,
  Correlativa
} from '../../../interfaces/interfaces'
import {
  TIPO_CORRELATIVA,
  REQUISITOS_CORRELATIVA,
  DatoListaInterface,
  MODOS_PROGRAMA_ASIGNATURA,
  ASIGNATURA_VACIA
} from '../../../constants/constants'
import {
  SeccionFormulario,
  BotonAgregarCorrelativa,
  ModalSeleccionCorrelativa
} from './SeccionFormulario'
import { MensajeDeError, TituloSeccion, Modal } from '../../../components'
import {
  CorrelativaAsignaturas,
  CorrelativaCantidad,
  CorrelativaModulo
} from './ObjetosListaCorrelativas'
import { concat } from 'lodash'

interface SeccionCorrelativasProps {
  programaAsignatura: ProgramaAsignaturaInterface
  setProgramaAsignatura: (
    programaAsignatura: ProgramaAsignaturaInterface
  ) => void
  modoProgramaAsignatura: string
  erroresSeccionCorrelativas: ProgramaAsignaturaErrores
  asignaturasDisponibles: DatoListaInterface[]
}

const SeccionCorrelativas: React.FC<SeccionCorrelativasProps> = ({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura,
  erroresSeccionCorrelativas,
  asignaturasDisponibles
}) => {
  const { correlativas } = programaAsignatura
  const [modalSeleccionAbierto, setModalSeleccionAbierto] =
    useState<boolean>(false)

  const asignaturasCorrelativasDisponibles = concat(
    [ASIGNATURA_VACIA],
    asignaturasDisponibles
  )

  const NUEVO_CORRELATIVA_ASIGNATURA: Correlativa = {
    id: null,
    requisito: REQUISITOS_CORRELATIVA.ASIGNATURA,
    tipo: TIPO_CORRELATIVA.NO_SELECCIONADO,
    asignatura: ASIGNATURA_VACIA
  }

  const NUEVO_CORRELATIVA_CANTIDAD: Correlativa = {
    id: null,
    requisito: REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS,
    tipo: TIPO_CORRELATIVA.NO_SELECCIONADO,
    cantidadAsignaturas: 0
  }

  const NUEVA_CORRELATIVA_MODULO: Correlativa = {
    id: null,
    requisito: REQUISITOS_CORRELATIVA.MODULO,
    tipo: TIPO_CORRELATIVA.NO_SELECCIONADO,
    modulo: ''
  }

  const modoLectura =
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER ||
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.REVISAR

  const handleSeleccionarCorrelativaAsignatura = (
    indice: number,
    asignaturaSeleccionada: number | string
  ) => {
    var correlativasModificadas = correlativas
    const objetoAsignaturaSeleccionada = asignaturasDisponibles.find(
      (dato) => dato.id == asignaturaSeleccionada
    )

    correlativasModificadas[indice] = {
      ...correlativasModificadas[indice],
      asignatura: objetoAsignaturaSeleccionada || ASIGNATURA_VACIA
    }

    setProgramaAsignatura({
      ...programaAsignatura,
      correlativas: correlativasModificadas
    })
  }

  const enCambioTipoCorrelativa = (
    indice: number,
    tipoCorrelativa: string | number
  ) => {
    const tipoSeleccionado =
      tipoCorrelativa === TIPO_CORRELATIVA.NO_SELECCIONADO
        ? TIPO_CORRELATIVA.NO_SELECCIONADO
        : tipoCorrelativa === TIPO_CORRELATIVA.APROBADO
          ? TIPO_CORRELATIVA.APROBADO
          : TIPO_CORRELATIVA.REGULAR

    var correlativasModificadas = correlativas
    correlativasModificadas[indice] = {
      ...correlativasModificadas[indice],
      tipo: tipoSeleccionado
    }

    setProgramaAsignatura({
      ...programaAsignatura,
      correlativas: correlativasModificadas
    })
  }

  const handleBorrarCorrelativa = (indice: number) => {
    var nuevasCorrelativas = correlativas
    nuevasCorrelativas.splice(indice, 1)
    setProgramaAsignatura({
      ...programaAsignatura,
      correlativas: nuevasCorrelativas
    })
  }

  const handleAgregarCorrelativa = () => {
    setModalSeleccionAbierto(true)
  }

  const handleCerrarModal = () => {
    setModalSeleccionAbierto(false)
  }

  const handleSeleccionRequisitoCorrelativa = (
    requisito: REQUISITOS_CORRELATIVA
  ) => {
    var correlativasModificadas = correlativas

    if (requisito === REQUISITOS_CORRELATIVA.ASIGNATURA) {
      correlativasModificadas.push(NUEVO_CORRELATIVA_ASIGNATURA)
    }
    if (requisito === REQUISITOS_CORRELATIVA.MODULO) {
      correlativasModificadas.push(NUEVA_CORRELATIVA_MODULO)
    }
    if (requisito === REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS) {
      correlativasModificadas.push(NUEVO_CORRELATIVA_CANTIDAD)
    }
    setProgramaAsignatura({
      ...programaAsignatura,
      correlativas: correlativasModificadas
    })
    handleCerrarModal()
  }

  const handleModificarCantidadAsignaturas = (
    indice: number,
    cantidad: string | number
  ) => {
    var cantidadNueva = undefined
    if (typeof cantidad === 'string') {
      cantidadNueva = parseInt(cantidad) || 0
    } else {
      cantidadNueva = cantidad
    }

    var correlativasModificadas = correlativas
    correlativasModificadas[indice] = {
      ...correlativasModificadas[indice],
      cantidadAsignaturas: cantidadNueva
    }

    setProgramaAsignatura({
      ...programaAsignatura,
      correlativas: correlativasModificadas
    })
  }

  const handleModificarModulo = (indice: number, modulo: string | number) => {
    var correlativasModificadas = correlativas
    correlativasModificadas[indice] = {
      ...correlativasModificadas[indice],
      modulo: modulo.toString()
    }

    setProgramaAsignatura({
      ...programaAsignatura,
      correlativas: correlativasModificadas
    })
  }

  return (
    <SeccionFormulario>
      <Modal
        open={modalSeleccionAbierto}
        onClose={handleCerrarModal}
        modalTitle="¿Qué tipo de correlativa desea agregar?"
      >
        <ModalSeleccionCorrelativa>
          <BotonAgregarCorrelativa
            onClick={() =>
              handleSeleccionRequisitoCorrelativa(
                REQUISITOS_CORRELATIVA.ASIGNATURA
              )
            }
          >
            Asignatura aprobada o regular
          </BotonAgregarCorrelativa>
          <BotonAgregarCorrelativa
            onClick={() =>
              handleSeleccionRequisitoCorrelativa(
                REQUISITOS_CORRELATIVA.CANTIDAD_ASIGNATURAS
              )
            }
          >
            Número de asignaturas aprobadas/regulares
          </BotonAgregarCorrelativa>
          <BotonAgregarCorrelativa
            onClick={() =>
              handleSeleccionRequisitoCorrelativa(REQUISITOS_CORRELATIVA.MODULO)
            }
          >
            Módulo aprobado o regular
          </BotonAgregarCorrelativa>
        </ModalSeleccionCorrelativa>
      </Modal>
      <TituloSeccion>CORRELATIVAS</TituloSeccion>
      {correlativas.map((correlativa, index) => {
        if (correlativa.requisito === REQUISITOS_CORRELATIVA.ASIGNATURA) {
          return (
            <CorrelativaAsignaturas
              modoLectura={modoLectura}
              key={`${programaAsignatura.id}${correlativa.id}`}
              tipo={correlativa.tipo}
              asignaturasDisponibles={asignaturasCorrelativasDisponibles}
              asignaturaSeleccionada={
                correlativa.asignatura?.id || ASIGNATURA_VACIA.id
              }
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
              key={`${programaAsignatura.id}${correlativa.id}`}
              cantidadAsignaturas={correlativa.cantidadAsignaturas || 0}
              tipo={correlativa.tipo}
              enCambioCantidadAsignaturas={(valor) =>
                handleModificarCantidadAsignaturas(index, valor)
              }
              enBorradoCorrelativa={() => handleBorrarCorrelativa(index)}
              enCambioTipoCorrelativa={(seleccion) =>
                enCambioTipoCorrelativa(index, seleccion)
              }
              modoLectura={modoLectura}
            />
          )
        }

        if (correlativa.requisito === REQUISITOS_CORRELATIVA.MODULO)
          return (
            <CorrelativaModulo
              key={`${programaAsignatura.id}${correlativa.id}`}
              modulo={correlativa.modulo || ''}
              tipo={correlativa.tipo}
              enCambioModulo={(modulo) => handleModificarModulo(index, modulo)}
              enBorradoCorrelativa={() => handleBorrarCorrelativa(index)}
              enCambioTipoCorrelativa={(seleccion) =>
                enCambioTipoCorrelativa(index, seleccion)
              }
              modoLectura={modoLectura}
            />
          )
      })}
      <MensajeDeError>{erroresSeccionCorrelativas.correlativas}</MensajeDeError>
      <BotonAgregarCorrelativa
        onClick={handleAgregarCorrelativa}
        disabled={modoLectura}
      >
        Agregar correlativa
      </BotonAgregarCorrelativa>
    </SeccionFormulario>
  )
}

export default SeccionCorrelativas
