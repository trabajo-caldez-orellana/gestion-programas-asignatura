import { useNavigate } from 'react-router-dom'

import './Tabla.css'
import {
  RUTAS_PAGINAS,
  MODOS_PROGRAMA_ASIGNATURA
} from '../../../../constants/constants'
import { TareaPendiente } from 'interfaces/interfaces'

interface PropiedadesTablaPendientes {
  datos: TareaPendiente[]
}

export default function Tabla({ datos }: PropiedadesTablaPendientes) {
  const navigate = useNavigate()

  const columnasTablaPendientes = [
    'ASIGNATURA',
    'TAREA PENDIENTE',
    'ACCIONES POSIBLES'
  ]

  const handleVerPrograma = (id: number | null) => {
    navigate(`${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${id}`)
  }

  const handleReutilizarUltimoPrograma = (id: number | null) => {
    console.log('reutilizar ultimo', id)
  }

  const handleModificarPrograma = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR}/${id}`
    )
  }

  const handleModificarAPartirUltimo = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO}/${id}`
    )
  }

  const handleCrearNuevoPrograma = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.NUEVO}/${id}`
    )
  }

  return (
    <article>
      <table className="content-table">
        <thead>
          <tr>
            {columnasTablaPendientes.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {datos.map((item) => (
            <tr key={item.asignatura.id}>
              <td>{item.asignatura.nombre}</td>
              <td>{item.accionRequerida}</td>
              <td id="column-acciones">
                {item.accionesPosibles && (
                  <>
                    {item.accionesPosibles.verPrograma && (
                      <i
                        onClick={() => handleVerPrograma(item.idPrograma)}
                        className="fas fa-eye boton-accion"
                        title="Ver programa"
                      ></i>
                    )}
                    {item.accionesPosibles.modificarPrograma && (
                      <i
                        onClick={() => handleModificarPrograma(item.idPrograma)}
                        className="fas fa-edit boton-accion"
                        title="Editar programa"
                      ></i>
                    )}
                    {item.accionesPosibles.reutilizarUltimo && (
                      <i
                        onClick={() =>
                          handleReutilizarUltimoPrograma(item.asignatura.id)
                        }
                        className="fas fa-redo boton-accion"
                        title="Usar ultimo programa"
                      ></i>
                    )}
                    {item.accionesPosibles.modificarUltimo && (
                      <i
                        onClick={() =>
                          handleModificarAPartirUltimo(item.asignatura.id)
                        }
                        className="fas fa-sync boton-accion"
                        title="Modificar a partir del ultimo program"
                      ></i>
                    )}
                    {item.accionesPosibles.nuevo && (
                      <i
                        onClick={() =>
                          handleCrearNuevoPrograma(item.asignatura.id)
                        }
                        className="fas fa-plus boton-accion"
                        title="Nuevo programa"
                      ></i>
                    )}
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
