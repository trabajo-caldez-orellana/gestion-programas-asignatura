import './Button.css'

interface ButtonProps {
  text: string
  onClick?: () => void
  link?: string
  cssClass?: string
  disabled?: boolean
}

export default function Button({ text, onClick, cssClass, disabled }: ButtonProps) {

  const buttonClass = `button ${cssClass || ''}`;

  return (
    <>
      <button type="button" onClick={onClick} className={buttonClass} disabled={disabled}>{text}</button>
    </>
  )
}
