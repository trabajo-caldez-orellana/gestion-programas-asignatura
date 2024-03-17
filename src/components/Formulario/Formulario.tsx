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
