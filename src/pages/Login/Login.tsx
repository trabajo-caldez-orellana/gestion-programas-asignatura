import React, {useState, useEffect, useCallback} from 'react'
import './Login.css'
import img from '../../img'
const BASE_FRONTEND_URL = import.meta.env.VITE_BASE_FRONTEND_URL
const CLIENT_ID = import.meta.env.VITE_GOOGLE_OAUTH2_CLIENT_ID

const Login: React.FC = () => {

  console.log("RENDERIZA LOGIN")

  const [username, setUsername] = useState(localStorage.getItem('goggleFirstName'))

  console.log('username', username)
  useEffect(() => {
    const storedUsername = localStorage.getItem("user_goggle");
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);
  const openGoogleLoginPage = useCallback(() => {
    const googleAuthUrl = "https://accounts.google.com/o/oauth2/v2/auth";
    
    const scope = [
      "https://www.googleapis.com/auth/userinfo.email",
      "https://www.googleapis.com/auth/userinfo.profile",
    ].join(" ");

    const params = new URLSearchParams({
      response_type: "code",
      client_id: CLIENT_ID,
      redirect_uri: `${BASE_FRONTEND_URL}/inicio`,
      prompt: "select_account",
      access_type: "offline",
      scope,
    });

    const url = `${googleAuthUrl}?${params}`;

    window.location.href = url;
  }, []);

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
        <button onClick={openGoogleLoginPage} className="login-button">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png" />
          <p>Iniciar sesion con Google</p>
        </button>
      </div>
    </div>
  )
}

export default Login
