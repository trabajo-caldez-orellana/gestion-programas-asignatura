import './Table.css'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../constants/constants'

type tableRow = {
  id: number | null
  asignatura: {
    id: number,
    nombre: string,
  }
  carrera: string
  estado: string
  id_programa: number | string | null 
  acciones_posibles: {
    ver_programa: boolean
    modificar_programa: boolean
    reutilizar_ultimo: boolean
    modificar_ultimo: boolean
    nuevo: boolean
  }
  accion_requerida: string | null
}

interface TableProps {
  tableColumns: string[]
  tableData: tableRow[]
  verPrograma: (id: number | null, modoPrograma: ModosProgramaAsignatura) => void
}

type ModosProgramaAsignatura = keyof typeof MODOS_PROGRAMA_ASIGNATURA;

// TODO: Esta tabla va a ser borrada dado que no se usara esta vista
export default function Table({
  tableColumns,
  tableData,
  verPrograma
}: TableProps) {
  // Si acciones no es null entonces renderizamos esa columna

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
              <td>{item.carrera}</td>
              <td>{item.asignatura.nombre}</td>
              <td>{item.estado}</td>
              <td>{item.id_programa}</td>
              <td id="column-acciones">
                {item.acciones_posibles ? (
                  <>
                    {item.acciones_posibles.ver_programa ? (
                      <i
                        onClick={() =>
                          verPrograma(item.id, MODOS_PROGRAMA_ASIGNATURA.VER as ModosProgramaAsignatura)
                        }
                        className="fas fa-eye"
                        title="Ver programa"
                      ></i>
                    ) : (
                      <></>
                    )}
                    {item.acciones_posibles.modificar_programa ? (
                      <i
                        onClick={() =>
                          verPrograma(item.id, MODOS_PROGRAMA_ASIGNATURA.EDITAR as ModosProgramaAsignatura)
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
                    {item.acciones_posibles.nuevo ? (
                      <i
                        onClick={() =>
                          verPrograma(item.id, MODOS_PROGRAMA_ASIGNATURA.NUEVO as ModosProgramaAsignatura)
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
