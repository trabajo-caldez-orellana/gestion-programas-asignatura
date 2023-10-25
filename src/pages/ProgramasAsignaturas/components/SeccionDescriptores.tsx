import { useState } from 'react'
import Button from '../../../components/ui/Button'
import Modal from '../../../components/Modal/Modal'
import { ProgramaAsignatura } from '../../../interfaces'
import camelCase from 'lodash/camelCase'

interface SeccionDescriptoresProps {
  programaAsignatura: ProgramaAsignatura
  setProgramaAsignatura: (programaAsignatura: ProgramaAsignatura) => void
}

export default function SeccionDescriptores({
  programaAsignatura,
  setProgramaAsignatura
}: SeccionDescriptoresProps) {
  const [modalResultadosAbierto, setModalResultadosAbierto] = useState(false)
  const [modalEjesTransversales, setModalEjesTransversales] = useState(false)

  const { descriptores } = programaAsignatura

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
    return programaAsignatura.descriptores.resultadosAprendizaje.filter(
      (item) => item !== ''
    ).length
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
    const resultadosAprendizaje = [...descriptores.resultadosAprendizaje]
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
    ejesTransversales[index].valor = parseInt(value)

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        ejesTransversales
      }
    })
  }

  const handleDescriptorChange = (id: number, tipo: string) => {
    const descriptoresCopy = { ...descriptores.descriptores }
    const sourceArray =
      tipo === 'si' ? descriptoresCopy.si : descriptoresCopy.no
    const targetArray =
      tipo === 'si' ? descriptoresCopy.no : descriptoresCopy.si

    const descriptorIndex = sourceArray.findIndex(
      (descriptor) => descriptor.id === id
    )

    if (descriptorIndex !== -1) {
      const descriptor = sourceArray[descriptorIndex]
      // Removemos el descriptor del array de origen y lo agregamos al array de destino
      sourceArray.splice(descriptorIndex, 1)
      targetArray.push(descriptor)
    }

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,
        descriptores: descriptoresCopy
      }
    })
  }

  return (
    <>
      <section className="form-section">
        <h2>Informacion Especifica</h2>
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
            />
            <Button text="+" />
          </div>
          <label htmlFor="descriptores">Descriptores</label>
          <br />
          <div className="selector-descritores">
            <div className="selector-descriptores-columna">
              <label>Si</label>

              {descriptores.descriptores.si.map((descriptor) => (
                <p onClick={() => handleDescriptorChange(descriptor.id, 'si')}>
                  {descriptor.nombre}
                </p>
              ))}
            </div>
            <div className="selector-descriptores-columna">
              <label>No</label>
              {descriptores.descriptores.no.map((descriptor) => (
                <p onClick={() => handleDescriptorChange(descriptor.id, 'no')}>
                  {descriptor.nombre}
                </p>
              ))}
            </div>
          </div>
        </form>
      </section>
      <Modal
        open={modalResultadosAbierto}
        modalTitle="Resultados de aprendizaje"
        onClose={() => setModalResultadosAbierto(false)}
      >
        {descriptores.resultadosAprendizaje.map((_, index) => (
          <>
            {/* {TODO: CREAR COMPONENTE} */}
            <textarea
              value={descriptores.resultadosAprendizaje[index]}
              onChange={(e) => handleResultadosAprendizajeChange(e, index)}
              rows={4}
              cols={50}
            />
            {index === descriptores.resultadosAprendizaje.length - 1 && (
              <div className="sumar-text-area">
                <Button text="+" onClick={aniadirResultadoAprendizaje}></Button>
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
                checked={eje.valor === 0}
                onChange={(e) => handleEjeTransversalChange(e, index)}
              />
              Nada
              <input
                type="radio"
                name={eje.nombre}
                value="1"
                checked={eje.valor === 1}
                onChange={(e) => handleEjeTransversalChange(e, index)}
              />
              Bajo
              <input
                type="radio"
                name={eje.nombre}
                value="2"
                checked={eje.valor === 2}
                onChange={(e) => handleEjeTransversalChange(e, index)}
              />
              Medio
              <input
                type="radio"
                name={eje.nombre}
                value="3"
                checked={eje.valor === 3}
                onChange={(e) => handleEjeTransversalChange(e, index)}
              />
              Alto
            </div>
          </>
        ))}
      </Modal>
    </>
  )
}
