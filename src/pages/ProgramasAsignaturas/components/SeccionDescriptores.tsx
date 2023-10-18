import { useState } from 'react'
import { camelCase } from 'lodash'
import Button from '../../../components/ui/Button'
import Modal from '../../../components/Modal/Modal'

export default function SeccionDescriptores() {
  const [isOpen, setIsOpen] = useState(false)
  const [formValues, setFormValues] = useState({
    resultadosAprendizaje: [],
    ejesTransversales: [],
    actividadesReservadas: []
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target

    setFormValues({
      ...formValues,
      [camelCase(name)]: value
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
              value={formValues.resultadosAprendizaje.length}
              onChange={handleChange}
            />
            <Button text="+" onClick={() => setIsOpen(true)} />
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
            <Button text="+" />
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
        </form>
      </section>
      <Modal open={isOpen} onClose={() => setIsOpen(false)}>
        MODAL
      </Modal>
    </>
  )
}
