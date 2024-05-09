import styled from 'styled-components'

export const SeccionFormulario = styled.section`
  width: 90%;
  padding: 30px;
  box-sizing: border-box;
  top: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  align-items: center;

  &.resultado-aprendizaje-text {
    width: 100%;
    min-height: 100px;
    padding: 8px;
    overflow-y: hidden;
    resize: none;
  }
`

export const InputOutsideContainer = styled.div`
  width: 100%;

  @media (min-width: 1100px) {
    width: 47%;
  }
`

export const WholeWidthInputContainer = styled.div`
  width: 100%;
`

export const BotonAgregarCorrelativa = styled.button`
  width: 100%;
  padding: 5px 10px;
  border: none;
  box-sizing: border-box;
  cursor: pointer;
  color: var(--primary-color);
  background-color: var(--secondary-color);

  margin-bottom: 5px;
  &:hover {
    background-color: var(--primary-color);
    color: white;
  }
`

export const ModalSeleccionCorrelativa = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 15px 10px;
`
