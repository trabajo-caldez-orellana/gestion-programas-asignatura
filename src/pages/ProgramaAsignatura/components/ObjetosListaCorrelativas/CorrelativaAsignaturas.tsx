import React from 'react'
import {
  DatoListaInterface,
  TIPO_CORRELATIVA,
  LISTADO_SELECCION_TIPOS_CORRELATIVA
} from '../../../../constants/constants'
import {
  CorrelativaContainer,
  BorrarCorrelativaButton
} from './CorrelativaStyled'
import { Dropdown } from '../../../../components'

interface CorrelativaAsignaturasInterface {
  asignaturaSeleccionada: number
  tipo: TIPO_CORRELATIVA
  asignaturasDisponibles: DatoListaInterface[]
  enCambioTipoCorrelativa: (seleccion: TIPO_CORRELATIVA) => void
  enCambioAsignaturaSeleccionada: (seleccion: number | string) => void
  enBorradoCorrelativa: () => void
}

const CorrelativaAsignaturas: React.FC<CorrelativaAsignaturasInterface> = ({
  asignaturaSeleccionada,
  tipo,
  asignaturasDisponibles,
  enCambioAsignaturaSeleccionada,
  enBorradoCorrelativa,
  enCambioTipoCorrelativa
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
      <div>
        <Dropdown
          name="tipoCorrelativa"
          value={tipo.valueOf()}
          error=""
          label="Tipo de Correlativa"
          choices={LISTADO_SELECCION_TIPOS_CORRELATIVA}
          onChange={handelModificarTipoDeCorrelativa}
        />
      </div>
      <div>
        <Dropdown
          name="Asignatura"
          value={asignaturaSeleccionada}
          error=""
          label="Asignatura"
          choices={asignaturasDisponibles}
          onChange={enCambioAsignaturaSeleccionada}
        />
      </div>
      <BorrarCorrelativaButton onClick={enBorradoCorrelativa}>
        <i className="fas fa-solid fa-trash" />
      </BorrarCorrelativaButton>
    </CorrelativaContainer>
  )
}

export default CorrelativaAsignaturas
