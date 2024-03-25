import ReactDom from 'react-dom'
import './Modal.css'
import Button from '../ui/Button'
import { ModalProps } from '../../constants/constants'

export default function Modal({
  open,
  children,
  modalTitle,
  onClose
}: ModalProps) {
  const portalRoot = document.getElementById('portal')
  if (!open || !portalRoot) return null

  return ReactDom.createPortal(
    <>
      <div className="overlay" />
      <div className="modal">
        <h2>{modalTitle}</h2>
        {children}
        <Button text="X" onClick={onClose} cssClass="close-modal-button" />
      </div>
    </>,
    portalRoot
  )
}
