import './Table.css'

type actions = {
  watch: boolean
  print: boolean
}

type tableRow = {
  id: number
  carrera: string
  version: string
  estado: string
}

interface TableProps {
  tableColumns: string[]
  tableData: tableRow[]
  acciones?: actions
  watch: (id: number) => void
}

export default function Table({
  tableColumns,
  tableData,
  acciones,
  watch
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
              <td>{item.version}</td>
              <td>{item.estado}</td>
              <td>
                <i onClick={() => watch(item.id)} className="fas fa-eye"></i>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
