import './Button.css'

interface ButtonProps {
  text: string
  onClick?: () => void
  link?: string
}

export default function Button({ text, onClick }: ButtonProps) {
  return (
    <>
      <button onClick={onClick} className='button'>{text}</button>
    </>
  )
}
