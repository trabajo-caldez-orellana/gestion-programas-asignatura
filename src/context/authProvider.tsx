import React, { createContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { client } from '../utils/axiosClient'

interface Auth {
  isLoggedIn: boolean
  userEmail: string | null
  userFirstName: string | null
  userLastName: string | null
  userProfilePicture: string | null
  userRoles: {
    es_docente: boolean
    es_administrador: boolean
    es_director_de_carrera: boolean
    es_secretario_academico: boolean
  }
}

interface AuthContextType {
  auth: Auth
  setAuth: React.Dispatch<React.SetStateAction<Auth>>
  handleLogout: () => void
  getAuthUser: () => void
  loading: boolean
  error: boolean
}

const defaultAuth: Auth = {
  isLoggedIn: false,
  userEmail: null,
  userFirstName: null,
  userLastName: null,
  userProfilePicture: null,
  userRoles: {
    es_administrador: false,
    es_director_de_carrera: false,
    es_docente: false,
    es_secretario_academico: false
  }
}

const AuthContext = createContext<AuthContextType>({
  auth: defaultAuth,
  setAuth: () => {},
  handleLogout: () => {},
  getAuthUser: () => {},
  loading: true,
  error: false
})

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [auth, setAuth] = useState<Auth>(defaultAuth)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const navigate = useNavigate()

  const handleLogout = async () => {
    const response = await client.get('auth/logout/')

    if (response.status === 200) {
      setAuth(defaultAuth)
      navigate('/')
    }
  }

  const getAuthUser = async () => {
    setLoading(true)
    client
      .get(`auth/me/`)
      .then((res) => {
        const { user, roles } = res.data.data
        setAuth({
          isLoggedIn: true,
          userEmail: user.email,
          userFirstName: user.first_name,
          userLastName: user.last_name,
          userProfilePicture: user.profile_picture,
          userRoles: roles
        })
        setLoading(false)
      })
      .catch((err) => {
        console.log('[ERROR ON AUTH]', err)
        setLoading(false)
        setError(true)
      })
  }

  useEffect(() => {
    getAuthUser()
  }, [])

  return (
    <AuthContext.Provider value={{ auth, setAuth, handleLogout, getAuthUser, loading, error}}>
      {children}
    </AuthContext.Provider>
  )
}
export { AuthContext, AuthProvider }
