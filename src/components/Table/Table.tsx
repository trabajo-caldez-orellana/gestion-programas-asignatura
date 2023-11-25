import './Table.css'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'

type actions = {
  watch: boolean
  print: boolean
}

type tableRow = {
  id: number
  asignatura: string
  carrera: string
  estado: string
  id_programa: number | null
  acciones_posibles: {
    ver: boolean
    editar: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    empezar_nuevo: boolean
  }
}

interface TableProps {
  tableColumns: string[]
  tableData: tableRow[]
  acciones?: actions
  verPrograma: (id: number, modoPrograma: string) => void
}

export default function Table({
  tableColumns,
  tableData,
  acciones,
  verPrograma
}: TableProps) {
  // Si acciones no es null entonces renderizamos esa columna
  if (acciones) {
    tableColumns.push('Acciones')
  }

  return (
    <article>
      <table className="content-table">
        <thead>
          <tr>
            {tableColumns.map((column) => (
              <th>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tableData.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.carrera}</td>
              <td>{item.estado}</td>
              <td>{item.id_programa}</td>
              <td id="column-acciones">
                {item.acciones_posibles ? (
                  <>
                    {item.acciones_posibles.ver ? (
                      <i
                        onClick={() =>
                          verPrograma(item.id, MODOS_PROGRAMA_ASIGNATURA.VER)
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
                          verPrograma(item.id, MODOS_PROGRAMA_ASIGNATURA.EDITAR)
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
                          verPrograma(item.id, MODOS_PROGRAMA_ASIGNATURA.NUEVO)
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
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
