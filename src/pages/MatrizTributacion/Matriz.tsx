import React from 'react'

import TablaPlanesEstudio from './TablasPlanesEstudio/TablaPlanesEstudio'
import usePlanesDeEstudio from './hooks/usePlanesDeEstudio'
import './Matriz.css'

const COLUMNAS_TABLA = ['Plan de Estudio', 'Carrera', 'Acciones']

const Matriz: React.FC = () => {
  const { loading, error, planesDeEstudio } = usePlanesDeEstudio()

  const handleGenerarMatriz = (idPlan: number, idCarrera: number) => {
    console.log(idPlan, idCarrera)
  }

  return (
    <div className="container-matriz">
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
