import { Button, MensajeDeError, Spinner } from '../../../components'
import { SeccionFormulario } from './SeccionFormulario'

interface BotonesProgramaAsignatura {
  error: string
  modoLectura: boolean
  handlePostPrograma: (isDraft: boolean) => () => void
  isLoading: boolean
}

export default function BotonesProgramaAsignatura({
  error,
  modoLectura,
  handlePostPrograma,
  isLoading
}: BotonesProgramaAsignatura) {
  if (modoLectura) return null

  return (
    <SeccionFormulario>
      {{ error } && <MensajeDeError>{error}</MensajeDeError>}
      <div className="acciones-programa-asignatura">
        {isLoading ? (
          <Spinner />
        ) : (
          <>
            <Button
              text="Guardar borrador"
              onClick={handlePostPrograma(false)}
            />
            <Button
              text="Enviar para aprobacion"
              onClick={handlePostPrograma(true)}
            />
          </>
        )}
      </div>
    </SeccionFormulario>
  )
}
