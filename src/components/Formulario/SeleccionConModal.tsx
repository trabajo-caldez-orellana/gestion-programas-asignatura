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
}

const SeleccionConModal: React.FC<SeleccionConModalInterface> = ({
  name,
  mensajeDeError,
  valorInput,
  isDisabled,
  children,
  tituloModal,
  onOpenModal
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
        onClose={handleCloseModal}
        open={modalAbierto}
        modalTitle={tituloModal}
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
