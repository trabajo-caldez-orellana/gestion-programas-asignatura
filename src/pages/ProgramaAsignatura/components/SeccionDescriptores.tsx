import { useState } from 'react'
import Button from '../../../components/ui/Button'
import Modal from '../../../components/Modal/Modal'
import { ProgramaAsignaturaInterface } from '../../../interfaces'
import camelCase from 'lodash/camelCase'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../../constants/constants'

interface SeccionDescriptoresProps {
  programaAsignatura: ProgramaAsignaturaInterface
  setProgramaAsignatura: (
    programaAsignatura: ProgramaAsignaturaInterface
  ) => void
  modoProgramaAsignatura: string
}

export default function SeccionDescriptores({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura
}: SeccionDescriptoresProps) {
  const [modalResultadosAbierto, setModalResultadosAbierto] = useState(false)
  const [modalEjesTransversales, setModalEjesTransversales] = useState(false)
  const [
    modalActividadesReservadasAbierto,
    setModalActividadesReservadasAbierto
  ] = useState(false)

  const { descriptores } = programaAsignatura
  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER

  const handleSeccionDescriptoresChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,
        [camelCase(name)]: value
      }
    })
  }

  const handleResultadosAprendizajeChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>,
    index: number
  ) => {
    const { value } = e.target

    const resultadosAprendizaje = [
      ...programaAsignatura.descriptores.resultadosAprendizaje
    ]
    resultadosAprendizaje[index] = value

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,
        resultadosAprendizaje: resultadosAprendizaje
      }
    })
  }

  const resultadosAprendizajeCount = () => {
    //Contar solo los resultados de aprendizaje que no sean string vacios
    const resultadosAprendizaje =
      programaAsignatura.descriptores.resultadosAprendizaje || []

    return resultadosAprendizaje.filter((item) => item !== '').length || 0
  }

  const aniadirResultadoAprendizaje = () => {
    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        resultadosAprendizaje: [
          ...programaAsignatura.descriptores.resultadosAprendizaje,
          ''
        ]
      }
    })
  }

  // Al abrir el modal limpiamos los resultados de aprendizaje que son string vacios
  const abrirModalResultados = () => {
    const resultadosAprendizaje: string[] =
      descriptores.resultadosAprendizaje || []
    const resultadosAprendizajeLimpios = resultadosAprendizaje.filter(
      (item) => item !== ''
    )
    if (resultadosAprendizajeLimpios.length === 0)
      resultadosAprendizajeLimpios.push('')

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        resultadosAprendizaje: resultadosAprendizajeLimpios
      }
    })
    setModalResultadosAbierto(true)
  }

  const handleEjeTransversalChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const { value } = e.target

    const ejesTransversales = [...descriptores.ejesTransversales]
    ejesTransversales[index].nivel = parseInt(value)

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        ejesTransversales
      }
    })
  }

  const handleDescriptorChange = (id: number) => {
    // Toggle the field seleccionado for the descriptor with the given id
    if (modoLectura) return
    const descriptores = [...programaAsignatura.descriptores.descriptores]
    const descriptor = descriptores.find((descriptor) => descriptor.id === id)
    if (descriptor) descriptor.seleccionado = !descriptor.seleccionado

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        descriptores
      }
    })
  }

  const handleActividadReservadaChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const { value } = e.target
    const actividadesReservadas = [...descriptores.actividadesReservadas]
    actividadesReservadas[index].nivel = parseInt(value)

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,
        actividadesReservadas
      }
    })
  }

  return (
    <>
      <section className="form-section">
        <h2 className="header">Informacion Especifica</h2>
        <form className="seccion-descriptores-form">
          <label htmlFor="resultados-aprendizaje">
            Resultados de aprendizaje
          </label>
          <div className="modal-input">
            <input
              type="text"
              id="resultados-aprendizaje"
              name="resultados_aprendizaje"
              value={resultadosAprendizajeCount()}
              onChange={handleSeccionDescriptoresChange}
              disabled={modoLectura}
            />
            <Button text="+" onClick={abrirModalResultados} />
          </div>
          <label htmlFor="ejes-transversales">Ejes transversales</label>
          <div className="modal-input">
            <input
              type="text"
              id="ejes-transversales"
              name="ejes_transversales"
              value={descriptores.ejesTransversales.length}
              onChange={handleSeccionDescriptoresChange}
              disabled={modoLectura}
            />
            <Button text="+" onClick={() => setModalEjesTransversales(true)} />
          </div>
          <label htmlFor="actividades-reservadas">Actividades reservadas</label>
          <div className="modal-input">
            <input
              type="text"
              id="actividades-reservadas"
              name="actividades_reservadas"
              value={descriptores.actividadesReservadas.length}
              onChange={handleSeccionDescriptoresChange}
              disabled={modoLectura}
            />
            <Button
              text="+"
              onClick={() => setModalActividadesReservadasAbierto(true)}
            />
          </div>
          <label htmlFor="descriptores">Descriptores</label>
          <br />
          <div className="selector-descritores">
            <div className="selector-descriptores-columna">
              <label>Si</label>

              {descriptores.descriptores.map(
                (descriptor) =>
                  descriptor.seleccionado && (
                    <p
                      key={descriptor.id}
                      onClick={() => handleDescriptorChange(descriptor.id)}
                    >
                      {descriptor.nombre}
                    </p>
                  )
              )}
            </div>
            <div className="selector-descriptores-columna">
              <label>No</label>
              {descriptores.descriptores.map(
                (descriptor) =>
                  !descriptor.seleccionado && (
                    <p
                      key={descriptor.id}
                      onClick={() => handleDescriptorChange(descriptor.id)}
                    >
                      {descriptor.nombre}
                    </p>
                  )
              )}
            </div>
          </div>
        </form>
      </section>
      <Modal
        open={modalResultadosAbierto}
        modalTitle="Resultados de aprendizaje"
        onClose={() => setModalResultadosAbierto(false)}
      >
        {descriptores.resultadosAprendizaje.map((resultado, index) => (
          <>
            {/* {TODO: CREAR COMPONENTE} */}
            <textarea
              key={index}
              value={resultado}
              onChange={(e) => handleResultadosAprendizajeChange(e, index)}
              rows={4}
              cols={50}
              disabled={modoLectura}
            />
            {index === descriptores.resultadosAprendizaje.length - 1 && (
              <div className="sumar-text-area">
                <Button
                  text="+"
                  onClick={aniadirResultadoAprendizaje}
                  disabled={modoLectura}
                ></Button>
              </div>
            )}
          </>
        ))}
      </Modal>
      <Modal
        open={modalEjesTransversales}
        modalTitle="Ejes transversales"
        onClose={() => setModalEjesTransversales(false)}
      >
        {descriptores.ejesTransversales.map((eje, index) => (
          <>
            <label>{eje.nombre}</label>
            {/* {TODO: CREAR COMPONENTE RADIO BUTTONS} */}

            <div className="radio-buttons">
              <input
                type="radio"
                name={eje.nombre}
                value="0"
                defaultChecked
                checked={eje.nivel === 0}
                onChange={(e) => handleEjeTransversalChange(e, index)}
                disabled={modoLectura}
              />
              Nada
              <input
                type="radio"
                name={eje.nombre}
                value="1"
                checked={eje.nivel === 1}
                onChange={(e) => handleEjeTransversalChange(e, index)}
                disabled={modoLectura}
              />
              Bajo
              <input
                type="radio"
                name={eje.nombre}
                value="2"
                checked={eje.nivel === 2}
                onChange={(e) => handleEjeTransversalChange(e, index)}
                disabled={modoLectura}
              />
              Medio
              <input
                type="radio"
                name={eje.nombre}
                value="3"
                checked={eje.nivel === 3}
                onChange={(e) => handleEjeTransversalChange(e, index)}
                disabled={modoLectura}
              />
              Alto
            </div>
          </>
        ))}
      </Modal>
      <Modal
        open={modalActividadesReservadasAbierto}
        modalTitle="Actividades Reservadas"
        onClose={() => setModalActividadesReservadasAbierto(false)}
      >
        {descriptores.actividadesReservadas.map((actividad, index) => (
          <>
            <label>{actividad.nombre}</label>
            {/* {TODO: CREAR COMPONENTE RADIO BUTTONS} */}

            <div className="radio-buttons">
              <input
                type="radio"
                name={actividad.nombre}
                value="0"
                defaultChecked
                checked={actividad.nivel === 0}
                onChange={(e) => handleActividadReservadaChange(e, index)}
                disabled={modoLectura}
              />
              Nada
              <input
                type="radio"
                name={actividad.nombre}
                value="1"
                checked={actividad.nivel === 1}
                onChange={(e) => handleActividadReservadaChange(e, index)}
                disabled={modoLectura}
              />
              Bajo
              <input
                type="radio"
                name={actividad.nombre}
                value="2"
                checked={actividad.nivel === 2}
                onChange={(e) => handleActividadReservadaChange(e, index)}
                disabled={modoLectura}
              />
              Medio
              <input
                type="radio"
                name={actividad.nombre}
                value="3"
                checked={actividad.nivel === 3}
                onChange={(e) => handleActividadReservadaChange(e, index)}
                disabled={modoLectura}
              />
              Alto
            </div>
          </>
        ))}
      </Modal>
    </>
  )
}
