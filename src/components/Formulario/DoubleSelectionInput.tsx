import React from 'react'

import {
  MensajeDeError,
  ContenedorLista,
  TituloLista,
  DoubleSelectionCoulmunsContainer,
  DoubleSelectionCoulumn,
  TituloColumna,
  ListadoColumna,
  Item
} from './Formulario'
import { DatosListaSeleccionInterface } from 'constants/constants'

interface DoubleSelectionInputInterface {
  titulo: string
  mensajeDeError: string
  handleListChange: (id: number) => void
  datosParaSeleccion: DatosListaSeleccionInterface[]
  modoLectura: boolean
}

const DoubleSelectionInput: React.FC<DoubleSelectionInputInterface> = ({
  titulo,
  mensajeDeError,
  handleListChange,
  datosParaSeleccion,
  modoLectura
}) => {
  return (
    <ContenedorLista>
      <TituloLista>{titulo}</TituloLista>
      {mensajeDeError && <MensajeDeError>{mensajeDeError}</MensajeDeError>}
      <DoubleSelectionCoulmunsContainer className="selector-descritores">
        <DoubleSelectionCoulumn className={modoLectura ? 'lectura' : ''}>
          <TituloColumna>Seleccionado</TituloColumna>
          <ListadoColumna>
            {datosParaSeleccion.map(
              (item) =>
                item.seleccionado && (
                  <Item key={item.id} onClick={() => handleListChange(item.id)}>
                    {item.informacion}
                  </Item>
                )
            )}
          </ListadoColumna>
        </DoubleSelectionCoulumn>
        {!modoLectura && (
          <DoubleSelectionCoulumn>
            <TituloColumna>No Seleccionado</TituloColumna>
            <ListadoColumna>
              {datosParaSeleccion.map(
                (item) =>
                  !item.seleccionado && (
                    <Item
                      key={item.id}
                      onClick={() => handleListChange(item.id)}
                    >
                      {item.informacion}
                    </Item>
                  )
              )}
            </ListadoColumna>
          </DoubleSelectionCoulumn>
        )}
      </DoubleSelectionCoulmunsContainer>
    </ContenedorLista>
  )
}

export default DoubleSelectionInput
