import { useState } from 'react'
import { camelCase } from 'lodash'
import Button from '../../../components/ui/Button'
import Modal from '../../../components/Modal/Modal'

// Definir type
type Descriptor = {
  resultadosAprendizaje: string[]
  ejesTransversales: {
    nombre: string
    valor: number
  }[]
  descriptores: {
    si: { id: number; nombre: string }[]
    no: { id: number; nombre: string }[]
  }
  actividadesReservadas: string[]
}

export default function SeccionDescriptores() {
  const [modalResultadosAbierto, setModalResultadosAbierto] = useState(false)
  const [modalEjesTransversales, setModalEjesTransversales] = useState(false)
  const [formValues, setFormValues] = useState<Descriptor>({
    resultadosAprendizaje: [''],
    ejesTransversales: [
      {
        nombre: 'Eje 1',
        valor: 0
      },

      {
        nombre: 'Eje 2',
        valor: 2
      }
    ],
    descriptores: {
      si: [
        { id: 1, nombre: 'Descriptor 1' },
        { id: 2, nombre: 'Descriptor 2' }
      ],
      no: [{ id: 3, nombre: 'Descriptor 3' }]
    },
    actividadesReservadas: []
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target

    setFormValues({
      ...formValues,
      [camelCase(name)]: value
    })
  }

  const handleResultadosAprendizajeChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>,
    index: number
  ) => {
    const { value } = e.target

    const resultadosAprendizaje = [...formValues.resultadosAprendizaje]
    resultadosAprendizaje[index] = value

    setFormValues({
      ...formValues,
      resultadosAprendizaje
    })
  }

  const resultadosAprendizajeCount = () => {
    //Contar solo los resultados de aprendizaje que no sean string vacios
    return formValues.resultadosAprendizaje.filter((item) => item !== '').length
  }

  const aniadirResultadoAprendizaje = () => {
    setFormValues({
      ...formValues,
      resultadosAprendizaje: [...formValues.resultadosAprendizaje, '']
    })
  }

  // Al abrir el modal limpiamos los resultados de aprendizaje que son string vacios
  const abrirModalResultados = () => {
    const resultadosAprendizaje = [...formValues.resultadosAprendizaje]
    const resultadosAprendizajeLimpios = resultadosAprendizaje.filter(
      (item) => item !== ''
    )
    if (resultadosAprendizajeLimpios.length === 0)
      resultadosAprendizajeLimpios.push('')

    setFormValues({
      ...formValues,
      resultadosAprendizaje: resultadosAprendizajeLimpios
    })
    setModalResultadosAbierto(true)
  }

  const handleEjeTransversalChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const { value } = e.target

    const ejesTransversales = [...formValues.ejesTransversales]
    ejesTransversales[index].valor = parseInt(value)

    setFormValues({
      ...formValues,
      ejesTransversales
    })
  }


  const handleDescriptorChange = (id: number, tipo: string) => {
    const descriptores = { ...formValues.descriptores };
    const sourceArray = tipo === 'si' ? descriptores.si : descriptores.no;
    const targetArray = tipo === 'si' ? descriptores.no : descriptores.si;
    
    const descriptorIndex = sourceArray.findIndex(descriptor => descriptor.id === id);
  
    if (descriptorIndex !== -1) {
      const descriptor = sourceArray[descriptorIndex];
      // Removemos el descriptor del array de origen y lo agregamos al array de destino
      sourceArray.splice(descriptorIndex, 1);
      targetArray.push(descriptor);
    }
  
    setFormValues({
      ...formValues,
      descriptores
    });
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
              onChange={handleChange}
            />
            <Button text="+" onClick={abrirModalResultados} />
          </div>
          <label htmlFor="ejes-transversales">Ejes transversales</label>
          <div className="modal-input">
            <input
              type="text"
              id="ejes-transversales"
              name="ejes_transversales"
              value={formValues.ejesTransversales.length}
              onChange={handleChange}
            />
            <Button text="+" onClick={() => setModalEjesTransversales(true)} />
          </div>
          <label htmlFor="actividades-reservadas">Actividades reservadas</label>
          <div className="modal-input">
            <input
              type="text"
              id="actividades-reservadas"
              name="actividades_reservadas"
              value={formValues.actividadesReservadas.length}
              onChange={handleChange}
            />
            <Button text="+" />
          </div>
          <label htmlFor="descriptores">Descriptores</label>
          <br />
          <div className="selector-descritores">
            <div className="selector-descriptores-columna">
              <label>Si</label>

              {formValues.descriptores.si.map((descriptor) => (
                <p onClick={() => handleDescriptorChange(descriptor.id, 'si')}>
                  {descriptor.nombre}
                </p>
              ))}
            </div>
            <div className="selector-descriptores-columna">
              <label>No</label>
              {formValues.descriptores.no.map((descriptor) => (
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
        {formValues.resultadosAprendizaje.map((_, index) => (
          <>
            {/* {TODO: CREAR COMPONENTE} */}
            <textarea
              value={formValues.resultadosAprendizaje[index]}
              onChange={(e) => handleResultadosAprendizajeChange(e, index)}
              rows={4}
              cols={50}
            />
            {index === formValues.resultadosAprendizaje.length - 1 && (
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
        {formValues.ejesTransversales.map((eje, index) => (
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
