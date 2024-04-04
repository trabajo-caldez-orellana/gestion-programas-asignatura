'use client'

import { LoadingCircle, SpinnerContainer } from './SpinnerStyled'

const Spinner: React.FC = () => {
  return (
    <SpinnerContainer>
      <LoadingCircle />
    </SpinnerContainer>
  )
}

export default Spinner
