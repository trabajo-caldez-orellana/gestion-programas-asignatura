import './Button.css'

interface ButtonProps {
  text: string
  onClick?: () => void
  link?: string
  cssClass?: string
}

export default function Button({ text, onClick, cssClass }: ButtonProps) {

  const buttonClass = `button ${cssClass || ''}`;

  return (
    <>
      <button type="button" onClick={onClick} className={buttonClass}>{text}</button>
    </>
  )
}
