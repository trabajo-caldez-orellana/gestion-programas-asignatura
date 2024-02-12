import Button from '../../../components/ui/Button'

interface BotonesProgramaAsignatura {
  errorPostProgramaAsignatura: boolean
  resultPostProgramaAsignatura: boolean
  modoLectura: boolean
  handlePostPrograma: (isDraft: boolean) => () => void
}

export default function BotonesProgramaAsignatura({
  errorPostProgramaAsignatura,
  resultPostProgramaAsignatura,
  modoLectura,
  handlePostPrograma
}: BotonesProgramaAsignatura) {
  if (errorPostProgramaAsignatura)
    return <p>Error al guardar el programa asignatura</p>

  if (resultPostProgramaAsignatura) return <p>Programa enviado correctamente</p>

  if (modoLectura) return null

  return (
    <div className="acciones-programa-asignatura">
      <Button text="Guardar borrador" onClick={handlePostPrograma(true)} />
      <Button
        text="Enviar para aprobacion"
        onClick={handlePostPrograma(false)}
      />
    </div>
  )
}
