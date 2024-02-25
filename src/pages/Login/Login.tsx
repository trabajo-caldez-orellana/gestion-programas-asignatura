import React from 'react'

import useGoogleAuthLink from '../../hooks/useGoogleAuthLink'
import './Login.css'
import img from '../../img'

const Login: React.FC = () => {
  const { refetch: fetchGoogleAuth } = useGoogleAuthLink()
  // Handlers
  const handleGoogleLogin = () => {
    fetchGoogleAuth()
  }
  return (
    <div className="container">
      <div className="card">
        <div className="profile-image">
          <i className="fas fa-user" />
        </div>

        <img className="logo-unt" src={img.UNT} />
        <img className="logo-facet" src={img.FACET} />
        <h1 className="title">Sistema de Gestion de Programas de Asignatura</h1>
        <h2 className="title">Facultad de Ciencias Exactas y Tecnología</h2>
        <h3 className="title">Universidad Nacional de Tucumán</h3>
        <p className="text">
          Para poder acceder a las funciones del sistema, debe iniciar sesión
          con Google. Si es su primera vez ingresando, debe comunicarse con el
          administrador del sistema para dar acceso.
        </p>
        <button onClick={handleGoogleLogin} className="login-button">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png" />
          <p>Iniciar sesion con Google</p>
        </button>
      </div>
    </div>
  )
}

export default Login
