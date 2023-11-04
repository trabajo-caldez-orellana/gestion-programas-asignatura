import { ProgramaAsignatura } from '../../../interfaces'
import camelCase from 'lodash/camelCase'

interface CargaHorariaProps {
  programaAsignatura: ProgramaAsignatura
  setProgramaAsignatura: (programaAsignatura: ProgramaAsignatura) => void
}

export default function CargaHoraria({
  programaAsignatura,
  setProgramaAsignatura
}: CargaHorariaProps) {
  const { cargaHoraria } = programaAsignatura

  const handleCargaHorariaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target

    setProgramaAsignatura({
      ...programaAsignatura,
      cargaHoraria: {
        ...programaAsignatura.cargaHoraria,
        [camelCase(name)]: value
      }
    })
  }

  return (
    <section className="form-section">
      <h2>Carga Horaria</h2>
      <form className="carga-horaria-form">
        {/* <label htmlFor="carga-horaria-total">Carga Horaria Total</label> */}
        {/* TODO: PONER EN UN MAP */}
        {/* <input
          type="text"
          id="carga-horaria-total"
          name="carga_horaria_total"
          value={cargaHoraria.cargaHorariaTotal}
          onChange={handleCargaHorariaChange}
        /> */}
        <label htmlFor="semanas-dictado">Semanas de dictado</label>
        <input
          type="text"
          id="semanas-dictado"
          name="semanas_dictado"
          value={cargaHoraria.semanasDictado}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="teoria-presencial">Teoria presencial</label>
        <input
          type="text"
          id="teoria-presencial"
          name="teoria_presencial"
          value={cargaHoraria.teoriaPresencial}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="practica-presencial">Practica presencial</label>
        <input
          type="text"
          id="practica-presencial"
          name="practica_presencial"
          value={cargaHoraria.practicaPresencial}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="teorico-practico-presencial">
          Teorico-practico presencial
        </label>
        <input
          type="text"
          id="teorico-practico-presencial"
          name="teorico_practico_presencial"
          value={cargaHoraria.teoricoPracticoPresencial}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="laboratorios-presenciales">
          Laboratorios presenciales
        </label>
        <input
          type="text"
          id="laboratorios-presenciales"
          name="laboratorios_presenciales"
          value={cargaHoraria.laboratoriosPresenciales}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="teoria-distancia">Teoria a distancia</label>
        <input
          type="text"
          id="teoria-distancia"
          name="teoria_distancia"
          value={cargaHoraria.teoriaDistancia}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="practica-distancia">Practica a distancia</label>
        <input
          type="text"
          id="practica-distancia"
          name="practica_distancia"
          value={cargaHoraria.practicaDistancia}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="teorico-practico-distancia">
          Teorico-practico a distancia
        </label>
        <input
          type="text"
          id="teorico-practico-distancia"
          name="teorico_practico_distancia"
          value={cargaHoraria.teoricoPracticoDistancia}
          onChange={handleCargaHorariaChange}
        />

        <label htmlFor="laboratorio-distancia">Laboratorio a distancia</label>
        <input
          type="text"
          id="laboratorio-distancia"
          name="laboratorio_distancia"
          value={cargaHoraria.laboratorioDistancia}
          onChange={handleCargaHorariaChange}
        />
      </form>
    </section>
  )
}
