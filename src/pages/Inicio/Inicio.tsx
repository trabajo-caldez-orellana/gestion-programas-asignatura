import React from 'react'
import useAuth from '../../hooks/useAuth'

const Inicio: React.FC = () => {
  const { auth } = useAuth()

  return <div>Bienvenido {auth.userFirstName}! :D</div>
}

export default Inicio
