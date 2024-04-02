import React, { createContext, useState, useEffect } from 'react'
import Cookies from 'js-cookie'
import { jwtDecode } from "jwt-decode";
import { client } from '../utils/axiosClient'

interface Auth {
  isLoggedIn: boolean
  userEmail: string | null
  userFirstName: string | null
  userLastName: string | null
}

interface AuthContextType {
  auth: Auth
  setAuth: React.Dispatch<React.SetStateAction<Auth>>
  handleLogout: () => void
}

const defaultAuth: Auth = {
  isLoggedIn: false,
  userEmail: null,
  userFirstName: null,
  userLastName: null
}

const AuthContext = createContext<AuthContextType>({
  auth: defaultAuth,
  setAuth: () => {},
  handleLogout: () => {}
})

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [auth, setAuth] = useState<Auth>(defaultAuth)

  const handleLogout = () => {
    Cookies.remove('token'); // Remueve el token
    Cookies.remove('refresh_token'); // Remueve el token

    window.location.href = '/login'
  }

  useEffect(() => {
    const authUser = async () => {
     client
     .get(`auth/me/`, {
       headers: {
         Authorization: `Bearer ${token}`
       }
     })
     .then((res) => {
       const { user } = res.data
       setAuth({
         isLoggedIn: true,
         userEmail: user.email,
         userFirstName: user.first_name,
         userLastName: user.last_name
       })
     })
     .catch((err) => {
       console.error('Error fetching user data:', err)
     })
    }

    const refreshToken = async () => {
      const refreshToken = Cookies.get('refresh_token');
      try {
          const res = await client.post("auth/token/refresh/", {
              refresh: refreshToken,
          });
          if (res.status === 200) {
            // Calcula la fecha dentro de 15 minutos
              const horaActual = new Date();
              const quinceMinutosDespues = new Date(horaActual.getTime() + 15 * 60 * 1000);
              Cookies.set('token', res.data.access, { expires: quinceMinutosDespues, secure: true });
          } else {
              // setIsAuthorized(false)
          }
      } catch (error) {
          console.log(error);
          // setIsAuthorized(false);
      }
    };

    const token = Cookies.get('token')

    if (!token || token && isTokenExpired(token)) {
      refreshToken()
    }

    authUser()


  }, [])

  const isTokenExpired = (token : string) => {
    const decoded = jwtDecode(token);
      const tokenExpiration = decoded.exp;
      const now = Date.now() / 1000;

      if (tokenExpiration) {
        return tokenExpiration < now;
      }
      return false;
  }


  return (
    <AuthContext.Provider value={{ auth, setAuth, handleLogout }}>
      {children}
    </AuthContext.Provider>
  )
}
export { AuthContext, AuthProvider }