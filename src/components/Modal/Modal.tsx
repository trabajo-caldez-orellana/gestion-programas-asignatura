import ReactDom from 'react-dom'
import './Modal.css'
import Button from '../ui/Button'
import { ModalProps } from '../../constants/constants'

export default function Modal({
  open,
  children,
  modalTitle,
  onClose,
  className = '',
  botonGuardado = false
}: ModalProps) {
  const portalRoot = document.getElementById('portal')
  if (!open || !portalRoot) return null

  return ReactDom.createPortal(
    <>
      <div className="overlay" />
      <div className={`modal ${className}`}>
        <h2>{modalTitle}</h2>
        {children}
        <Button
          text={botonGuardado ? 'Guardar' : 'X'}
          onClick={onClose}
          cssClass="close-modal-button"
        />
      </div>
    </>,
    portalRoot
  )
}
