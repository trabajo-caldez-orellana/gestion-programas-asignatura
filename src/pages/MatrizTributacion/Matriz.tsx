import React, { useState } from 'react'

import TablaPlanesEstudio from './TablasPlanesEstudio/TablaPlanesEstudio'
import usePlanesDeEstudio from './hooks/usePlanesDeEstudio'
import { getMatrizDeTributacion } from './servicios'
import { Modal } from '../../components'
import './Matriz.css'

const COLUMNAS_TABLA = ['Plan de Estudio', 'Carrera', 'Acciones']

const Matriz: React.FC = () => {
  const [modalIsOpen, setModalIsOpen] = useState<boolean>(false)
  const { loading, error, planesDeEstudio } = usePlanesDeEstudio()
  const [mensajeDeError, setMensajeDeError] = useState<string>('')

  const handleGenerarMatriz = (idPlan: number, idCarrera: number) => {
    getMatrizDeTributacion(idPlan, idCarrera).then((response) => {
      if (response.status === 200 && response.data) {
        setModalIsOpen(false)

        // Crear un objeto URL con los datos del archivo
        const url = window.URL.createObjectURL(new Blob([response.data]))

        // Crear un enlace temporal
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'matriz-tributacion.csv')

        // Simular clic en el enlace para iniciar la descarga
        document.body.appendChild(link)
        link.click()

        // Limpiar el objeto URL y el enlace
        window.URL.revokeObjectURL(url)
        document.body.removeChild(link)
      } else if (response.status === 400 && response.error) {
        if (response.error.all) {
          setMensajeDeError(response.error.all)
        } else {
          setMensajeDeError('Error inesperado. Intente nuevamente más tarde')
        }

        setModalIsOpen(true)
      } else {
        setMensajeDeError('Error inesperado. Intente nuevamente más tarde')
        setModalIsOpen(true)
      }
    })
  }

  return (
    <div className="container-matriz">
      <Modal
        open={modalIsOpen}
        onClose={() => setModalIsOpen(false)}
        modalTitle="Ocurrió un Error"
      >
        <div>{mensajeDeError}</div>
      </Modal>
      <div className="cabecera-matriz">
        <h1 className="titulo-matriz">Generar Reportes</h1>
        <h2 className="subtitulo-matriz">Matriz de Tributación</h2>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <div>{error}</div>
      ) : (
        <div className="tabla-planes">
          <TablaPlanesEstudio
            tableColumns={COLUMNAS_TABLA}
            tableData={planesDeEstudio}
            generarMatriz={handleGenerarMatriz}
          />
        </div>
      )}
    </div>
  )
}

export default Matriz
