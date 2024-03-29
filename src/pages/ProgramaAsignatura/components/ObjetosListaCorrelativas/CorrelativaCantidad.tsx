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
  enCambioTipoCorrelativa: (seleccion: TIPO_CORRELATIVA) => void
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
  const handelModificarTipoDeCorrelativa = (
    valorCorrelativa: string | number
  ) => {
    if (!valorCorrelativa) {
      return
    }
    const tipoCorrelativa =
      valorCorrelativa === TIPO_CORRELATIVA.APROBADO
        ? TIPO_CORRELATIVA.APROBADO
        : TIPO_CORRELATIVA.REGULAR
    enCambioTipoCorrelativa(tipoCorrelativa)
  }

  return (
    <CorrelativaContainer>
      <InfoContainer>
        <Dropdown
          name="tipoCorrelativa"
          value={tipo.valueOf()}
          error=""
          label="Tipo de Correlativa"
          choices={LISTADO_SELECCION_TIPOS_CORRELATIVA}
          onChange={handelModificarTipoDeCorrelativa}
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
