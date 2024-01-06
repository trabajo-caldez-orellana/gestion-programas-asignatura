import './Tabla.css'

import { TareaPendiente } from 'interfaces/interfaces'

interface PropiedadesTablaPendientes {
  datos: TareaPendiente[]
}

export default function Tabla({ datos }: PropiedadesTablaPendientes) {
  // Si acciones no es null entonces renderizamos esa columna

  const columnasTablaPendientes = [
    'ASIGNATURA',
    'TAREA PENDIENTE',
    'ACCIONES POSIBLES'
  ]

  return (
    <article>
      <table className="content-table">
        <thead>
          <tr>
            {columnasTablaPendientes.map((column) => (
              <th>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {datos.map((item) => (
            <tr key={item.asignatura.id}>
              <td>{item.asignatura.nombre}</td>
              <td>{item.accionRequerida}</td>
              <td id="column-acciones">
                Acciones posibles
                {/* {item.acciones_posibles ? (
                  <>
                    {item.acciones_posibles.ver ? (
                      <i
                        onClick={() =>
                          verPrograma(
                            item.id,
                            MODOS_PROGRAMA_ASIGNATURA.VER as ModosProgramaAsignatura
                          )
                        }
                        className="fas fa-eye"
                        title="Ver programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.acciones_posibles.editar ? (
                      <i
                        onClick={() =>
                          verPrograma(
                            item.id,
                            MODOS_PROGRAMA_ASIGNATURA.EDITAR as ModosProgramaAsignatura
                          )
                        }
                        className="fas fa-edit"
                        title="Editar programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.acciones_posibles.reutilizar_ultimo ? (
                      <i
                        className="fas fa-redo"
                        title="Usar ultimo programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.acciones_posibles.modificar_ultimo ? (
                      <i
                        className="fas fa-sync"
                        title="Modificar ultimo program"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.acciones_posibles.empezar_nuevo ? (
                      <i
                        onClick={() =>
                          verPrograma(
                            item.id,
                            MODOS_PROGRAMA_ASIGNATURA.NUEVO as ModosProgramaAsignatura
                          )
                        }
                        className="fas fa-plus"
                        title="Nuevo programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                  </>
                ) : (
                  <></>
                )} */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
