import { Button, MensajeDeError } from '../../../components'
import { SeccionFormulario } from './SeccionFormulario'

interface BotonesProgramaAsignatura {
  error: string
  modoLectura: boolean
  handlePostPrograma: (isDraft: boolean) => () => void
}

export default function BotonesProgramaAsignatura({
  error,
  modoLectura,
  handlePostPrograma
}: BotonesProgramaAsignatura) {
  if (modoLectura) return null

  return (
    <SeccionFormulario>
      {{ error } && <MensajeDeError>{error}</MensajeDeError>}
      <div className="acciones-programa-asignatura">
        <Button text="Guardar borrador" onClick={handlePostPrograma(false)} />
        <Button
          text="Enviar para aprobacion"
          onClick={handlePostPrograma(true)}
        />
      </div>
    </SeccionFormulario>
  )
}
