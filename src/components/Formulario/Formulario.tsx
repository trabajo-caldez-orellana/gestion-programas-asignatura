import styled from 'styled-components'

export const Formulario = styled.form`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
  box-sizing: border-box;
  margin: 20px 0 0;
  justify-content: space-between;
`

export const MensajeDeError = styled.span`
  color: brown;
  max-width: 500px;
  width: 60%;
  padding: 5px 10px;
`

export const TextAreaLabel = styled.label`
  background-color: var(--primary-color);
  color: white;
  padding: 5px 10px;
`

export const TextAreaStyled = styled.textarea`
  border: none;
  background-color: #00000022;
  padding: 5px 10px;
`

export const SectionDivider = styled.hr`
  height: 5px;
  width: 90%;
  background-color: var(--secondary-color);
  border: none;
`

export const TextAreaContainer = styled.div`
  display: flex;
  width: 100%;
  flex-direction: column;
  justify-content: center;
  margin: 10px auto;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const InputContainer = styled.div`
  display: flex;
  width: 100%;
  flex-direction: row;
  margin: 10px auto;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const LabelContainer = styled.div`
  display: flex;
  width: 30%;
  flex-direction: column;
  justify-content: center;
  border-radius: 5px;
  margin: 10px auto;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const InputLabel = styled.label`
  background-color: var(--primary-color);
  color: white;
  width: 30%;
  padding: 5px 10px;
`

export const InputStyled = styled.input`
  border: none;
  width: 70%;
  background-color: #00000022;
  padding: 5px 10px;
  color: black;
`

export const ContenedorLista = styled.div`
  display: flex;
  width: 100%;
  flex-direction: column;
  margin: 10px auto;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const TituloLista = styled.h4`
  background-color: var(--primary-color);
  color: white;
  padding: 5px 10px;
  font-weight: 400;
`

export const Listado = styled.ul`
  border: none;
  width: 100%;
  background-color: #00000022;
  list-style: none;
`

export const Item = styled.li`
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;

  &:hover {
    background-color: #00000022;
  }
`

export const ModalInputContainer = styled.div`
  width: 100%;
  display: flex;
  margin: 10px auto;
  flex-direction: column;

  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const SeleccionConModalLabel = styled.label`
  background-color: var(--primary-color);
  color: white;
  padding: 5px 10px;
  width: 100%;
`

export const ModalInputSection = styled.div`
  display: flex;
  width: 100%;
`

export const ModalInput = styled.input`
  width: 80%;
  padding: 5px 10px;
  border: none;
  box-sizing: border-box;
  background-color: #00000022;
`

export const ModalInputButton = styled.button`
  margin: 0;
  box-sizing: border-box;
  color: var(--primary-color);
  background-color: var(--secondary-color);
  width: 20%;
  border: none;
`

export const DoubleSelectionCoulmunsContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: row;
`

export const ListadoColumna = styled.li`
  border: none;
  width: 100%;
  list-style: none;
`

export const DoubleSelectionCoulumn = styled.div`
  width: 50%;
  background-color: #00000022;
`

export const TituloColumna = styled(TituloLista)`
  background-color: var(--secondary-color);
  color: var(--primary-color);
`

export const DropdownContainer = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
`

export const SelectStyled = styled.select`
  color: black;
  width: 100%;
  padding: 5px 10px;
  font-size: 16px;
  text-align: center;
  border: none;
  cursor: pointer;
  background-color: var(--contrast-color);

  &::placeholder {
    text-transform: uppercase;
    color: white;
    opacity: 0.9;
  }
`

interface TieneErrorInterface {
  $tieneError: boolean
}

export const InputButtonContainer = styled.div<TieneErrorInterface>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
  border: 2px solid ${(props) => (props.$tieneError ? 'red' : 'none')};
`
