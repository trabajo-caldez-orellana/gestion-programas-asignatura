import { camelCase } from 'lodash'
import { ProgramaAsignatura } from '../../../interfaces'
import { MODOS_PROGRAMA_ASIGNATURA } from '../../../constants/constants'

interface InformacionAdicionalProps {
  programaAsignatura: ProgramaAsignatura
  setProgramaAsignatura: (programaAsignatura: ProgramaAsignatura) => void
  modoProgramaAsignatura: string
}

export default function InformacionAdicional({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura
}: InformacionAdicionalProps) {
  const { informacionAdicional } = programaAsignatura
  const modoLectura = modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER


  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = e.target

    setProgramaAsignatura({
      ...programaAsignatura,
      informacionAdicional: {
        ...programaAsignatura.informacionAdicional,
        [camelCase(name)]: value
      }
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
          value={informacionAdicional.fundamentacion}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />
        <label htmlFor="contenidos">Contenidos</label>
        <textarea
          id="contenidos"
          name="contenidos"
          value={informacionAdicional.contenidos}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />

        <label htmlFor="bibliografia">Bibliografia</label>
        <textarea
          id="bibliografia"
          name="bibliografia"
          value={informacionAdicional.bibliografia}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />

        <label htmlFor="metodologia-aplicada">Metodologia aplicada</label>
        <textarea
          id="metodologia-aplicada"
          name="metodologia_aplicada"
          value={informacionAdicional.metodologiaAplicada}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />

        <label htmlFor="recursos">Recursos</label>
        <textarea
          id="recursos"
          name="recursos"
          value={informacionAdicional.recursos}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />

        <label htmlFor="evaluacion">Evaluacion</label>
        <textarea
          id="evaluacion"
          name="evaluacion"
          value={informacionAdicional.evaluacion}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />

        <label htmlFor="investigacion">Investigacion</label>
        <textarea
          id="investigacion"
          name="investigacion"
          value={informacionAdicional.investigacion}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />

        <label htmlFor="extension">Extension</label>
        <textarea
          id="extension"
          name="extension"
          value={informacionAdicional.extension}
          onChange={handleChange}
          rows={4}
          cols={50}
          disabled={modoLectura}
        />
      </form>
    </section>
  )
}
