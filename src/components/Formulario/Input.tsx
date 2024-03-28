import React from 'react'

import {
  MensajeDeError,
  InputStyled,
  InputLabel,
  InputContainer
} from './Formulario'

interface InputTextoInterface {
  name: string
  id: string
  value: string | number
  type: string
  label: string
  mensajeDeError: string
  onChange: (name: string | number, value: string) => void
  modoLectura: boolean
}

const Input: React.FC<InputTextoInterface> = ({
  name,
  id,
  value,
  type,
  label,
  mensajeDeError,
  onChange,
  modoLectura
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(name, e.target.value)
  }

  return (
    <>
      <InputContainer>
        <InputLabel htmlFor={id}>{label}</InputLabel>
        <InputStyled
          type={type}
          id={id}
          name={name}
          onChange={handleChange}
          disabled={modoLectura}
          value={value}
        />
      </InputContainer>
      {mensajeDeError && <MensajeDeError>{mensajeDeError}</MensajeDeError>}
    </>
  )
}

export default Input
