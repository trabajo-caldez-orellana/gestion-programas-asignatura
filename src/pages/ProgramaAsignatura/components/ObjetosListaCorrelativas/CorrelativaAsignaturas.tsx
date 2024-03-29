import React from 'react'
import {
  DatoListaInterface,
  TIPO_CORRELATIVA,
  LISTADO_SELECCION_TIPOS_CORRELATIVA
} from '../../../../constants/constants'
import {
  CorrelativaContainer,
  BorrarCorrelativaButton,
  InfoContainer
} from './CorrelativaStyled'
import { Dropdown } from '../../../../components'

interface CorrelativaAsignaturasInterface {
  asignaturaSeleccionada: number
  tipo: TIPO_CORRELATIVA
  asignaturasDisponibles: DatoListaInterface[]
  enCambioTipoCorrelativa: (seleccion: TIPO_CORRELATIVA) => void
  enCambioAsignaturaSeleccionada: (seleccion: number | string) => void
  enBorradoCorrelativa: () => void
  modoLectura: boolean
}

const CorrelativaAsignaturas: React.FC<CorrelativaAsignaturasInterface> = ({
  asignaturaSeleccionada,
  tipo,
  asignaturasDisponibles,
  enCambioAsignaturaSeleccionada,
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
        <Dropdown
          name="Asignatura"
          value={asignaturaSeleccionada}
          error=""
          label="Asignatura"
          choices={asignaturasDisponibles}
          onChange={enCambioAsignaturaSeleccionada}
          modoLectura={modoLectura}
        />
      </InfoContainer>
      <BorrarCorrelativaButton onClick={enBorradoCorrelativa}>
        <i className="fas fa-solid fa-trash" />
      </BorrarCorrelativaButton>
    </CorrelativaContainer>
  )
}

export default CorrelativaAsignaturas
