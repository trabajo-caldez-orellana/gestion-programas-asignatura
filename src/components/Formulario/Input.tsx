import React from 'react'

interface InputTextoInterface {
  name: string
  id: string
  value: string | number
  type: string
  onChange: (name: string, value: string) => void
}

const Input: React.FC<InputTextoInterface> = ({
  name,
  id,
  value,
  onChange
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(name, e.target.value)
  }

  return <div>Input</div>
}

export default Input
