import { useState } from 'react'
import { camelCase } from 'lodash'

export default function InformacionAdicional() {
  const [formValues, setFormValues] = useState({
    fundamentacion: '',
    contenidos: '',
    bibliografia: '',
    metodologiaAplicada: '',
    recursos: '',
    evaluacion: '',
    investigacion: '',
    extension: ''
  })

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = e.target

    setFormValues({
      ...formValues,
      [camelCase(name)]: value
    })
  }

  return (
    <section className="form-section">
      <h2>Carga Horaria</h2>
      <form className="informacion-adicional-form">
        <label htmlFor="fundamentacion">Fundamentacion</label>
        <textarea
          id="fundamentacion"
          name="fundamentacion"
          value={formValues.fundamentacion}
          onChange={handleChange}
          rows={4}
          cols={50}
        />
        <label htmlFor="contenidos">Contenidos</label>
        <textarea
          id="contenidos"
          name="contenidos"
          value={formValues.contenidos}
          onChange={handleChange}
          rows={4}
          cols={50}
        />

        <label htmlFor="bibliografia">Bibliografia</label>
        <textarea
          id="bibliografia"
          name="bibliografia"
          value={formValues.bibliografia}
          onChange={handleChange}
          rows={4}
          cols={50}
        />

        <label htmlFor="metodologia-aplicada">Metodologia aplicada</label>
        <textarea
          id="metodologia-aplicada"
          name="metodologia_aplicada"
          value={formValues.metodologiaAplicada}
          onChange={handleChange}
          rows={4}
          cols={50}
        />

        <label htmlFor="recursos">Recursos</label>
        <textarea
          id="recursos"
          name="recursos"
          value={formValues.recursos}
          onChange={handleChange}
          rows={4}
          cols={50}
        />

        <label htmlFor="evaluacion">Evaluacion</label>
        <textarea
          id="evaluacion"
          name="evaluacion"
          value={formValues.evaluacion}
          onChange={handleChange}
          rows={4}
          cols={50}
        />

        <label htmlFor="investigacion">Investigacion</label>
        <textarea
          id="investigacion"
          name="investigacion"
          value={formValues.investigacion}
          onChange={handleChange}
          rows={4}
          cols={50}
        />

        <label htmlFor="extension">Extension</label>
        <textarea
          id="extension"
          name="extension"
          value={formValues.extension}
          onChange={handleChange}
          rows={4}
          cols={50}
        />
      </form>
    </section>
  )
}
