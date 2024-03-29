import React from 'react'
import {
  TIPO_CORRELATIVA,
  LISTADO_SELECCION_TIPOS_CORRELATIVA
} from '../../../../constants/constants'
import {
  CorrelativaContainer,
  BorrarCorrelativaButton,
  InfoContainer
} from './CorrelativaStyled'
import { Input, Dropdown } from '../../../../components'

interface CorrelativaAsignaturasInterface {
  cantidadAsignaturas: number
  tipo: TIPO_CORRELATIVA
  enCambioTipoCorrelativa: (seleccion: number | string) => void
  enCambioCantidadAsignaturas: (valor: number | string) => void
  enBorradoCorrelativa: () => void
  modoLectura: boolean
}

const CorrelativaCantidad: React.FC<CorrelativaAsignaturasInterface> = ({
  cantidadAsignaturas,
  tipo,
  enCambioCantidadAsignaturas,
  enBorradoCorrelativa,
  enCambioTipoCorrelativa,
  modoLectura
}) => {
  return (
    <CorrelativaContainer>
      <InfoContainer>
        <Dropdown
          name="tipoCorrelativa"
          value={tipo.valueOf()}
          error=""
          label="Tipo de Correlativa"
          choices={LISTADO_SELECCION_TIPOS_CORRELATIVA}
          onChange={enCambioTipoCorrelativa}
          modoLectura={modoLectura}
        />
      </InfoContainer>
      <InfoContainer>
        <Input
          id="cantidad"
          type="number"
          name="cantidad"
          mensajeDeError=""
          value={cantidadAsignaturas}
          label="Cantidad asignaturas"
          onChange={enCambioCantidadAsignaturas}
          modoLectura={modoLectura}
        />
      </InfoContainer>
      <BorrarCorrelativaButton onClick={enBorradoCorrelativa}>
        <i className="fas fa-solid fa-trash" />
      </BorrarCorrelativaButton>
    </CorrelativaContainer>
  )
}

export default CorrelativaCantidad
