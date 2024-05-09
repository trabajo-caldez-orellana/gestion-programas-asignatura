import { useNavigate } from 'react-router-dom'

import { Spinner } from '../../../../components'
import './Tabla.css'
import {
  RUTAS_PAGINAS,
  MODOS_PROGRAMA_ASIGNATURA
} from '../../../../constants/constants'
import useTareasPendientes from '../../hooks/useTareasPendientes'

export default function Tabla() {
  const { tareasPendientes, loading, error } = useTareasPendientes()

  const navigate = useNavigate()

  const columnasTablaPendientes = [
    'ASIGNATURA',
    'TAREA PENDIENTE',
    'ACCIONES POSIBLES'
  ]

  const handleVerPrograma = (id: number | null) => {
    navigate(`${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${id}`)
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

  const handleRevisarPrograma = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.REVISAR}/${id}`
    )
  }

  return loading ? (
    <div
      style={{
        width: '300px',
        height: '300px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '0 auto'
      }}
    >
      <Spinner />
    </div>
  ) : (
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
          {tareasPendientes.length > 0 ? (
            <>
              {tareasPendientes.map((item) => (
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
                            onClick={() =>
                              handleModificarPrograma(item.idPrograma)
                            }
                            className="fas fa-edit boton-accion"
                            title="Editar programa"
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
                        {item.accionesPosibles.revisarPrograma && (
                          <i
                            onClick={() =>
                              handleRevisarPrograma(item.idPrograma)
                            }
                            className="fas fa-check boton-accion"
                            title="Revisar programa"
                          ></i>
                        )}
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </>
          ) : error ? (
            <tr>
              <td>Ocurrió un error al momento de realizar la búsqueda</td>
            </tr>
          ) : (
            <tr>
              <td>No hay datos que coincidan con la búsqueda</td>
            </tr>
          )}
        </tbody>
      </table>
    </article>
  )
}
