import React, { useEffect, useRef } from 'react'
import {
  TextAreaLabel,
  MensajeDeError,
  TextAreaStyled,
  TextAreaContainer
} from './Formulario'

interface TextAreaTextoInterface {
  name: string
  id: string
  value: string
  mensajeDeError: string
  label: string
  onChange: (name: string, value: string) => void
  modoLectura: boolean
}

const TextArea: React.FC<TextAreaTextoInterface> = ({
  name,
  id,
  value,
  mensajeDeError,
  label,
  onChange,
  modoLectura
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (textareaRef.current?.style) {
      textareaRef.current.style.height = 'auto' // Reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight + textareaRef.current.style.lineHeight}px` // Set new height
    }
  }, [textareaRef.current?.scrollHeight])

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(name, e.target.value)
  }

  return (
    <TextAreaContainer>
      <TextAreaLabel htmlFor={id} key={id}>
        {label}
      </TextAreaLabel>
      <TextAreaStyled
        id={id}
        name={name}
        value={value}
        onChange={handleChange}
        disabled={modoLectura}
        ref={textareaRef}
      />
      {mensajeDeError && <MensajeDeError>{mensajeDeError}</MensajeDeError>}
    </TextAreaContainer>
  )
}

export default TextArea
