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
  modulo: string
  tipo: TIPO_CORRELATIVA
  enCambioTipoCorrelativa: (seleccion: TIPO_CORRELATIVA) => void
  enCambioModulo: (valor: number | string) => void
  enBorradoCorrelativa: () => void
  modoLectura: boolean
}

const CorrelativaModulo: React.FC<CorrelativaAsignaturasInterface> = ({
  modulo,
  tipo,
  enCambioModulo,
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
          id="modulo"
          type="text"
          name="modulo"
          mensajeDeError=""
          value={modulo}
          label="Módulo"
          onChange={enCambioModulo}
          modoLectura={modoLectura}
        />
      </InfoContainer>
      <BorrarCorrelativaButton onClick={enBorradoCorrelativa}>
        <i className="fas fa-solid fa-trash" />
      </BorrarCorrelativaButton>
    </CorrelativaContainer>
  )
}

export default CorrelativaModulo
