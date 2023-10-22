import ReactDom from 'react-dom'
import './Modal.css'

interface ModalProps {
  open: boolean
  children: React.ReactNode
  onClose: () => void
}

export default function Modal({ open, children, onClose }: ModalProps) {
  const portalRoot = document.getElementById('portal')
  if (!open || !portalRoot) return null

  return ReactDom.createPortal(
    <>
      <div className="overlay" />
      <div className="modal">
        <button onClick={onClose}>Close Modal</button>
        {children}
      </div>
    </>,
    portalRoot
  )
}
