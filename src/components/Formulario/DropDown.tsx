import {
  DropdownContainer,
  SelectStyled,
  MensajeDeError,
  InputButtonContainer,
  InputLabel
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
  modoLectura: boolean
}

const Dropdown: React.FC<DropdownInterface> = ({
  name,
  label,
  value,
  error,
  choices,
  onChange,
  modoLectura
}) => {
  const handleValueChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(e.target.value)
  }

  return (
    <DropdownContainer>
      <InputLabel>{label}</InputLabel>
      <InputButtonContainer $tieneError={!!error}>
        <SelectStyled
          name={name}
          value={value}
          onChange={handleValueChange}
          disabled={modoLectura}
        >
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
