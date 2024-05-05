import { Spinner } from '../../../components'
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
  imprimir: (
    id: number | string | null,
    modoPrograma: ModosProgramaAsignatura
  ) => void
  isLoading: boolean
  error: boolean
}

type ModosProgramaAsignatura = keyof typeof MODOS_PROGRAMA_ASIGNATURA

export default function TableHistorial({
  tableColumns,
  tableData,
  verPrograma,
  imprimir,
  isLoading,
  error
}: TableProps) {
  // Si acciones no es null entonces renderizamos esa columna

  return isLoading ? (
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
            {tableColumns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {tableData && tableData.length > 0 ? (
            <>
              {tableData.map((item) => (
                <tr key={item.id}>
                  <td>{item.asignatura.nombre}</td>
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
                            style={{ cursor: 'pointer' }}
                          ></i>
                        ) : null}
                        {item.acciones_posibles.imprimir ? (
                          <i
                            onClick={() =>
                              imprimir(
                                item.id,
                                MODOS_PROGRAMA_ASIGNATURA.IMPRIMIR as ModosProgramaAsignatura
                              )
                            }
                            className="fas fa-print"
                            style={{ cursor: 'pointer' }}
                            title="Imprimir"
                          ></i>
                        ) : null}
                      </>
                    ) : null}
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
