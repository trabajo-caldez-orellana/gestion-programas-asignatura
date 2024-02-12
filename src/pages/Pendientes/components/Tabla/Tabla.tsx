import './Tabla.css'

import { TareaPendiente } from 'interfaces/interfaces'

interface PropiedadesTablaPendientes {
  datos: TareaPendiente[]
}

export default function Tabla({ datos }: PropiedadesTablaPendientes) {
  const columnasTablaPendientes = [
    'ASIGNATURA',
    'TAREA PENDIENTE',
    'ACCIONES POSIBLES'
  ]

  const handleVerPrograma = (id: number | null) => {
    console.log('Ver programa numero ', id)
  }

  const handleReutilizarUltimoPrograma = (id: number | null) => {
    console.log('Reutilizar ultimo', id)
  }

  const handleModificarPrograma = (id: number | null) => {
    console.log('Modificar programa', id)
  }

  const handleModificarAPartirUltimo = (id: number | null) => {
    console.log('Modificar programa a partir del ultimo', id)
  }

  const handleCrearNuevoPrograma = (id: number | null) => {
    console.log('Crear nuevo programa', id)
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
                {item.accionesPosibles ? (
                  <>
                    {item.accionesPosibles.verPrograma ? (
                      <i
                        onClick={() => handleVerPrograma(item.idPrograma)}
                        className="fas fa-eye boton-accion"
                        title="Ver programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.modificarPrograma ? (
                      <i
                        onClick={() => handleModificarPrograma(item.idPrograma)}
                        className="fas fa-edit boton-accion"
                        title="Editar programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.reutilizarUltimo ? (
                      <i
                        onClick={() =>
                          handleReutilizarUltimoPrograma(item.asignatura.id)
                        }
                        className="fas fa-redo boton-accion"
                        title="Usar ultimo programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.modificarUltimo ? (
                      <i
                        onClick={() =>
                          handleModificarAPartirUltimo(item.asignatura.id)
                        }
                        className="fas fa-sync boton-accion"
                        title="Modificar a partir del ultimo program"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.accionesPosibles.nuevo ? (
                      <i
                        onClick={() =>
                          handleCrearNuevoPrograma(item.asignatura.id)
                        }
                        className="fas fa-plus boton-accion"
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
