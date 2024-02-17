import Button from '../../../components/ui/Button'

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
    <>
      {{ error } && <div className="mensaje-error">{error}</div>}
      <div className="acciones-programa-asignatura">
        <Button text="Guardar borrador" onClick={handlePostPrograma(true)} />
        <Button
          text="Enviar para aprobacion"
          onClick={handlePostPrograma(false)}
        />
      </div>
    </>
  )
}
