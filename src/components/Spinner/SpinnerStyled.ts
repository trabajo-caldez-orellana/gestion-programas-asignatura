import styled from 'styled-components'

export const SpinnerContainer = styled.div`
  width: 100vw;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`

export const LoadingCircle = styled.img`
  width: 50px;
  height: 50px;
  padding: 30px;
  border: 5px solid white;
  border-bottom-color: var(--primary-color);
  border-left-color: var(--primary-color);
  border-right-color: var(--primary-color);
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: spin 2s linear infinite;

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  &.modal-styles {
    position: absolute;
    bottom: 20px;
    right: 20px;
  }
`
