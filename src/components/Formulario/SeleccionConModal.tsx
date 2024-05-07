import React, { useState } from 'react'

import {
  MensajeDeError,
  ModalInputContainer,
  SeleccionConModalLabel,
  ModalInputSection,
  ModalInput,
  ModalInputButton
} from './Formulario'
import Modal from '../Modal/Modal'

interface SeleccionConModalInterface {
  name: string
  mensajeDeError: string
  valorInput: number
  isDisabled: boolean
  children: React.ReactNode
  tituloModal: string
  onOpenModal?: () => void
  className?: string
}

const SeleccionConModal: React.FC<SeleccionConModalInterface> = ({
  name,
  mensajeDeError,
  valorInput,
  isDisabled,
  children,
  tituloModal,
  onOpenModal,
  className = ''
}) => {
  const [modalAbierto, setModalAbierto] = useState<boolean>(false)

  const handleOpenModal = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()

    if (onOpenModal) {
      onOpenModal()
    }
    setModalAbierto(true)
  }
  const handleCloseModal = () => {
    setModalAbierto(false)
  }

  return (
    <ModalInputContainer>
      <Modal
        className={className}
        onClose={handleCloseModal}
        open={modalAbierto}
        modalTitle={tituloModal}
        botonGuardado={true}
      >
        {children}
      </Modal>
      <SeleccionConModalLabel htmlFor={name}>
        {tituloModal}
      </SeleccionConModalLabel>
      <ModalInputSection>
        <ModalInput
          type="text"
          id={name}
          name={name}
          value={valorInput}
          disabled={isDisabled}
          readOnly={true}
        />
        <ModalInputButton onClick={handleOpenModal}>+</ModalInputButton>
      </ModalInputSection>
      {mensajeDeError && <MensajeDeError>{mensajeDeError}</MensajeDeError>}
    </ModalInputContainer>
  )
}

export default SeleccionConModal
