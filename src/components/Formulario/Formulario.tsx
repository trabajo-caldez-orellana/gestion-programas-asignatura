import styled from 'styled-components'

export const Formulario = styled.form`
  display: flex;
  flex-direction: column;
  width: 100%;
  box-sizing: border-box;
  margin: 20px 0 0;
`

export const MensajeDeError = styled.span`
  color: brown;
  max-width: 500px;
  width: 60%;
  padding: 5px 10px;
`

export const InputLabel = styled.label`
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
  border-radius: 5px;
  margin: 10px auto;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`
