import React from 'react'

import { ContenedorLista, TituloLista, Listado, Item } from './Formulario'
import { DatoListaInterface } from '../../constants/constants'

interface ListadoDatosInterface {
  tituloListado: string
  datos: DatoListaInterface[]
}

const ListadoDatos: React.FC<ListadoDatosInterface> = ({
  datos,
  tituloListado
}) => {
  return (
    <ContenedorLista>
      <TituloLista>{tituloListado}</TituloLista>
      <Listado>
        {datos.map((dato) => (
          <Item key={dato.id}>{dato.informacion}</Item>
        ))}
      </Listado>
    </ContenedorLista>
  )
}

export default ListadoDatos
