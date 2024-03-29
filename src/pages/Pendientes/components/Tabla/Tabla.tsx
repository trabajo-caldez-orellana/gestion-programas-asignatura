import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Modal } from '../../../../components'
import './Tabla.css'
import {
  RUTAS_PAGINAS,
  MODOS_PROGRAMA_ASIGNATURA
} from '../../../../constants/constants'
import { reutilizarUltimoPrograma } from '../../services'
import useTareasPendientes from '../../hooks/useTareasPendientes'

export default function Tabla() {
  const { tareasPendientes, refetchTareas } = useTareasPendientes()

  const navigate = useNavigate()
  const [cargando, setCargando] = useState<boolean>(false)
  const [modalAbierto, setModalAbierto] = useState<boolean>(false)
  const [mensajeRespuesta, setMensajeRespuesta] = useState<string>('')

  const columnasTablaPendientes = [
    'ASIGNATURA',
    'TAREA PENDIENTE',
    'ACCIONES POSIBLES'
  ]

  const handleVerPrograma = (id: number | null) => {
    navigate(`${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${id}`)
  }

  const handleReutilizarUltimoPrograma = async (id: number | null) => {
    setCargando(true)
    setModalAbierto(true)
    setMensajeRespuesta('')

    if (id) {
      const response = await reutilizarUltimoPrograma(id)
      if (response.status === 200) {
        setMensajeRespuesta('Programa reutilizado con exito.')
        refetchTareas()
      } else {
        if (response.error) {
          setMensajeRespuesta(response.error)
        } else {
          setMensajeRespuesta('Error inesperado. Intente nuevamente más tarde.')
        }
      }

      setCargando(false)
      return
    }

    setCargando(false)
    setMensajeRespuesta('No se selcciono ninguna asignatura')
  }

  const handleModificarPrograma = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR}/${id}`
    )
  }

  const handleModificarAPartirUltimo = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO}/${id}`
    )
  }

  const handleCrearNuevoPrograma = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.NUEVO}/${id}`
    )
  }

  const handleRevisarPrograma = (id: number | null) => {
    navigate(
      `${RUTAS_PAGINAS.PROGRAMA_DE_ASIGNATURA}/${MODOS_PROGRAMA_ASIGNATURA.REVISAR}/${id}`
    )
  }

  return (
    <article>
      <Modal
        open={modalAbierto}
        onClose={() => setModalAbierto(false)}
        modalTitle="Reutilizar Ultimo Programa"
      >
        {cargando ? 'Cargando...' : mensajeRespuesta}
      </Modal>
      <table className="content-table">
        <thead>
          <tr>
            {columnasTablaPendientes.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {tareasPendientes.map((item) => (
            <tr key={item.asignatura.id}>
              <td>{item.asignatura.nombre}</td>
              <td>{item.accionRequerida}</td>
              <td id="column-acciones">
                {item.accionesPosibles && (
                  <>
                    {item.accionesPosibles.verPrograma && (
                      <i
                        onClick={() => handleVerPrograma(item.idPrograma)}
                        className="fas fa-eye boton-accion"
                        title="Ver programa"
                      ></i>
                    )}
                    {item.accionesPosibles.modificarPrograma && (
                      <i
                        onClick={() => handleModificarPrograma(item.idPrograma)}
                        className="fas fa-edit boton-accion"
                        title="Editar programa"
                      ></i>
                    )}
                    {item.accionesPosibles.reutilizarUltimo && (
                      <i
                        onClick={() =>
                          handleReutilizarUltimoPrograma(item.asignatura.id)
                        }
                        className="fas fa-redo boton-accion"
                        title="Usar ultimo programa"
                      ></i>
                    )}
                    {item.accionesPosibles.modificarUltimo && (
                      <i
                        onClick={() =>
                          handleModificarAPartirUltimo(item.asignatura.id)
                        }
                        className="fas fa-sync boton-accion"
                        title="Modificar a partir del ultimo program"
                      ></i>
                    )}
                    {item.accionesPosibles.nuevo && (
                      <i
                        onClick={() =>
                          handleCrearNuevoPrograma(item.asignatura.id)
                        }
                        className="fas fa-plus boton-accion"
                        title="Nuevo programa"
                      ></i>
                    )}
                    {item.accionesPosibles.revisarPrograma && (
                      <i
                        onClick={() => handleRevisarPrograma(item.idPrograma)}
                        className="fas fa-check boton-accion"
                        title="Revisar programa"
                      ></i>
                    )}
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </article>
  )
}
