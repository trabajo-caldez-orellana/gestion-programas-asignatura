import React, { createContext, useState, useEffect } from 'react'
import axios from 'axios'
import Cookies from 'js-cookie'
import { jwtDecode } from "jwt-decode";

interface Auth {
  isLoggedIn: boolean
  userEmail: string | null
  userFirstName: string | null
  userLastName: string | null
}

interface AuthContextType {
  auth: Auth
  setAuth: React.Dispatch<React.SetStateAction<Auth>>
}

const defaultAuth: Auth = {
  isLoggedIn: false,
  userEmail: null,
  userFirstName: null,
  userLastName: null
}

const AuthContext = createContext<AuthContextType>({
  auth: defaultAuth,
  setAuth: () => {}
})

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [auth, setAuth] = useState<Auth>(defaultAuth)

  useEffect(() => {
    const authUser = async () => {
     axios
     .get(`http://127.0.0.1:8000/auth/me/`, {
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
          const res = await axios.post("http://127.0.0.1:8000/auth/token/refresh/", {
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
    <AuthContext.Provider value={{ auth, setAuth }}>
      {children}
    </AuthContext.Provider>
  )
}
export { AuthContext, AuthProvider }
