import {
  DropdownContainer,
  SelectStyled,
  MensajeDeError,
  InputButtonContainer,
  TextAreaLabel
} from './Formulario'

interface ChoicesForDropdown {
  id: number | string
  informacion: string
}

interface DropdownInterface {
  name: string
  label: string
  value: number | string
  error: string
  choices: ChoicesForDropdown[]
  onChange: (value: number | string) => void
}

const Dropdown: React.FC<DropdownInterface> = ({
  name,
  label,
  value,
  error,
  choices,
  onChange
}) => {
  const handleValueChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(e.target.value)
  }

  return (
    <DropdownContainer>
      <TextAreaLabel>{label}</TextAreaLabel>
      <InputButtonContainer $tieneError={!!error}>
        <SelectStyled name={name} value={value} onChange={handleValueChange}>
          {choices.map((choice) => (
            <option key={choice.id} value={choice.id}>
              {choice.informacion}
            </option>
          ))}
        </SelectStyled>
      </InputButtonContainer>
      {!!error && <MensajeDeError>{error}</MensajeDeError>}
    </DropdownContainer>
  )
}

export default Dropdown
