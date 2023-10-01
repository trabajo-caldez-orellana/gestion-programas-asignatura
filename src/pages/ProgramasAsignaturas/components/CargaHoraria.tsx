import { useState } from 'react'
import { camelCase } from 'lodash'

export default function CargaHoraria() {
  const [formValues, setFormValues] = useState({
    cargaHorariaTotal: 0,
    semanasDictado: 0,
    teoriaPresencial: 0,
    practicaPresencial: 0,
    teoricoPracticoPresencial: 0,
    laboratoriosPresenciales: 0,
    teoriaDistancia: 0,
    practicaDistancia: 0,
    teoricoPracticoDistancia: 0,
    laboratorioDistancia: 0
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target

    setFormValues({
      ...formValues,
      [camelCase(name)]: value
    })
  }

  return (
    <section className="form-section">
      <h2>Carga Horaria</h2>
      <form className="carga-horaria-form">
        <label htmlFor="carga-horaria-total">Carga Horaria Total</label>
        <input
          type="text"
          id="carga-horaria-total"
          name="carga_horaria_total"
          value={formValues.cargaHorariaTotal}
          onChange={handleChange}
        />
        <label htmlFor="semanas-dictado">Semanas de dictado</label>
        <input
          type="text"
          id="semanas-dictado"
          name="semanas_dictado"
          value={formValues.semanasDictado}
          onChange={handleChange}
        />

        <label htmlFor="teoria-presencial">Teoria presencial</label>
        <input
          type="text"
          id="teoria-presencial"
          name="teoria_presencial"
          value={formValues.teoriaPresencial}
          onChange={handleChange}
        />

        <label htmlFor="practica-presencial">Practica presencial</label>
        <input
          type="text"
          id="practica-presencial"
          name="practica_presencial"
          value={formValues.practicaPresencial}
          onChange={handleChange}
        />

        <label htmlFor="teorico-practico-presencial">
          Teorico-practico presencial
        </label>
        <input
          type="text"
          id="teorico-practico-presencial"
          name="teorico_practico_presencial"
          value={formValues.teoricoPracticoPresencial}
          onChange={handleChange}
        />

        <label htmlFor="laboratorios-presenciales">
          Laboratorios presenciales
        </label>
        <input
          type="text"
          id="laboratorios-presenciales"
          name="laboratorios_presenciales"
          value={formValues.laboratoriosPresenciales}
          onChange={handleChange}
        />

        <label htmlFor="teoria-distancia">Teoria a distancia</label>
        <input
          type="text"
          id="teoria-distancia"
          name="teoria_distancia"
          value={formValues.teoriaDistancia}
          onChange={handleChange}
        />

        <label htmlFor="practica-distancia">Practica a distancia</label>
        <input
          type="text"
          id="practica-distancia"
          name="practica_distancia"
          value={formValues.practicaDistancia}
          onChange={handleChange}
        />

        <label htmlFor="teorico-practico-distancia">
          Teorico-practico a distancia
        </label>
        <input
          type="text"
          id="teorico-practico-distancia"
          name="teorico_practico_distancia"
          value={formValues.teoricoPracticoDistancia}
          onChange={handleChange}
        />

        <label htmlFor="laboratorio-distancia">Laboratorio a distancia</label>
        <input
          type="text"
          id="laboratorio-distancia"
          name="laboratorio_distancia"
          value={formValues.laboratorioDistancia}
          onChange={handleChange}
        />
      </form>
    </section>
  )
}
