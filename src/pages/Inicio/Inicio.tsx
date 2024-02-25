import React from 'react'
import useProfile from '../../hooks/useProfile'

const Inicio: React.FC = () => {
  const { profileData } = useProfile()

  return <div>Bienvenido {profileData?.firstName}! :D</div>
}

export default Inicio
