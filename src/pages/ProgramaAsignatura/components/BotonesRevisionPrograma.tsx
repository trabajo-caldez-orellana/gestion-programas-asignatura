import { useState } from 'react'
import Button from '../../../components/ui/Button'
import { Modal } from '../../../components'

interface BotonesProgramaAsignatura {
  error: string
  handleAprobarPrograma: () => void
  handlePedirCambiosPrograma: (mensaje: string) => void
}

export default function BotonesRevisionProgramaAsignatura({
  error,
  handleAprobarPrograma,
  handlePedirCambiosPrograma
}: BotonesProgramaAsignatura) {
  const [modalAbierto, setModalAbierto] = useState<boolean>(false)
  const [mensajeDeCambios, setMensajeDeCambios] = useState<string>('')

  const handleChangeMensajeDeCambios = (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setMensajeDeCambios(e.target.value)
  }

  const handleBotonPedirCambios = () => {
    handlePedirCambiosPrograma(mensajeDeCambios)
  }

  return (
    <>
      {{ error } && <div className="mensaje-error">{error}</div>}
      <Modal
        modalTitle="Mensaje de Cambios"
        open={modalAbierto}
        onClose={() => setModalAbierto(false)}
      >
        {/*
          Usar nuevo componente de textarea
        */}
        <textarea
          onChange={handleChangeMensajeDeCambios}
          value={mensajeDeCambios}
        />
        <Button text="PEDIR CAMBIOS" onClick={handleBotonPedirCambios} />
      </Modal>
      <div className="acciones-programa-asignatura">
        <Button text="APROBAR" onClick={handleAprobarPrograma} />
        <Button text="PEDIR CAMBIOS" onClick={() => setModalAbierto(true)} />
      </div>
    </>
  )
}
