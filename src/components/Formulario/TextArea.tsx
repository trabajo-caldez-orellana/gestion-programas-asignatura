import React from 'react'
import {
  InputLabel,
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
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(name, e.target.value)
  }

  return (
    <TextAreaContainer>
      <InputLabel htmlFor={id} key={id}>
        {label}
      </InputLabel>
      <TextAreaStyled
        id={id}
        name={name}
        value={value}
        onChange={handleChange}
        rows={4}
        cols={50}
        disabled={modoLectura}
      />
      {mensajeDeError && <MensajeDeError>{mensajeDeError}</MensajeDeError>}
    </TextAreaContainer>
  )
}

export default TextArea
