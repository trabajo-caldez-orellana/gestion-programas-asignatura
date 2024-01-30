import '../../../components/Table/Table.css'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../../constants/constants'
import { tableRowProgramasVigentes } from 'props/props'

interface TableProps {
  tableColumns: string[]
  tableData: tableRowProgramasVigentes[] | null
  verPrograma: (
    id: number | null,
    modoPrograma: ModosProgramaAsignatura
  ) => void
}

type ModosProgramaAsignatura = keyof typeof MODOS_PROGRAMA_ASIGNATURA

export default function TableHistorial({
  tableColumns,
  tableData,
  verPrograma
}: TableProps) {
  // Si acciones no es null entonces renderizamos esa columna

  if (!tableData) {
    return <h1>No hay datos</h1>
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
              <td>{item.asignatura.nombre}</td>
              <td>{item.estado}</td>
              <td id="column-acciones">
                {item.acciones_posibles ? (
                  <>
                    {item.acciones_posibles.ver_programa ? (
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
                    ) : null}
                    {item.acciones_posibles.imprimir ? (
                      <i
                        //   TODO: Agregar onclick xd
                        className="fas fa-print"
                        title="Imprimir"
                      ></i>
                    ) : null}
                  </>
                ) : null}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
