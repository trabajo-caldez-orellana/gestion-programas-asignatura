import { PlanesDeEstudioInterface } from 'interfaces/interfaces'

interface TableProps {
  tableColumns: string[]
  tableData: PlanesDeEstudioInterface[]
  generarMatriz: (id_plan: number, id_carrera: number) => void
}

// TODO: Esta tabla va a ser borrada dado que no se usara esta vista
export default function TablaPlanesEstudio({
  tableColumns,
  tableData,
  generarMatriz
}: TableProps) {
  return (
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
          {tableData.map((item) => (
            <tr key={item.id}>
              <td>{item.nombre}</td>
              <td>{item.carreraNombre}</td>
              <td id="column-acciones">
                <i
                  style={{ cursor: 'pointer' }}
                  className="fa fa-file-excel"
                  onClick={() => generarMatriz(item.id, item.carreraId)}
                  title="Generar Matriz"
                ></i>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
