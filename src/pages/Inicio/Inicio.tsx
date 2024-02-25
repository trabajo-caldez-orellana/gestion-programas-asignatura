import React from 'react'
import useProfile from '../../hooks/useProfile'

const Inicio: React.FC = () => {
  const { data: profile } = useProfile()

  return <div>Bienvenido {profile?.firstName}! :D</div>
}

export default Inicio
