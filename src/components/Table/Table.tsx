import './Table.css'

type actions = {
  watch: boolean
  print: boolean
}

type tableRow = {
  id: number,
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
              <td>{item.estado}</td>
              <td>{item.id_programa}</td>
              <td id="column-acciones">
                {
                  item.acciones_posibles ? (
                    <>
                      {item.acciones_posibles.ver ? <i onClick={() => watch(item.id)} className="fas fa-eye"></i> : <></>}
                      {item.acciones_posibles.editar ? <i className="fas fa-edit"></i> : <></>}
                      {item.acciones_posibles.reutilizar_ultimo ? <i className="fas fa-redo"></i> : <></>}
                      {item.acciones_posibles.modificar_ultimo ? <i className="fas fa-edit"></i> : <></>}
                      {item.acciones_posibles.empezar_nuevo ? <i className="fas fa-plus"></i> : <></>}
                    </>
                  ) : <></>
                }
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
