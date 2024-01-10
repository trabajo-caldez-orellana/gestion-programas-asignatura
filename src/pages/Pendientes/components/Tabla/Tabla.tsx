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

  const handleVerPrograma = (id: number | null) => {
    console.log('Ver programa numero ', id)
  }

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
                {item.accionesPosibles ? (
                  <>
                    {item.accionesPosibles.verPrograma ? (
                      <i
                        onClick={() => handleVerPrograma(item.idPrograma)}
                        className="fas fa-eye"
                        title="Ver programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.modificarPrograma ? (
                      <i
                        onClick={() => handleVerPrograma(item.idPrograma)}
                        className="fas fa-edit"
                        title="Editar programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.reutilizarUltimo ? (
                      <i
                        className="fas fa-redo"
                        title="Usar ultimo programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.modificarUltimo ? (
                      <i
                        className="fas fa-sync"
                        title="Modificar ultimo program"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.nuevo ? (
                      <i
                        onClick={() => handleVerPrograma(item.idPrograma)}
                        className="fas fa-plus"
                        title="Nuevo programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                  </>
                ) : (
                  <></>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
