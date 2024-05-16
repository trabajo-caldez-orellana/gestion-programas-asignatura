// import { PropsWithChildren, useEffect, useState } from 'react'
import { PropsWithChildren, useState, useEffect } from 'react'

import { useNavigate, useLocation } from 'react-router-dom'

import { RUTAS_PAGINAS } from '../../constants/constants'
import useAuth from '../../hooks/useAuth'
import Spinner from '../Spinner/Spinner'

const RUTAS_DESPROTEGIDAS = [RUTAS_PAGINAS.LOGIN, RUTAS_PAGINAS.LOGIN_LOADING, '/']

const ProtectedRoute: React.FC<PropsWithChildren> = ({ children }) => {
  const { auth, loading } = useAuth()

  const navigate = useNavigate()
  const location = useLocation()

  const [isReadyToRender, setIsReadyToRender] = useState<boolean>(false)

  useEffect(() => {
    const pathname = location.pathname
    // Si la autenticación está en proceso, no hacer nada
    if (loading) return

    if (auth.isLoggedIn) {
      // Si el usuario está autenticado, renderizar el componente

      // Si el usuario está en la página de login o una pagina sin permisos, redirigir a la página de inicio
      if (pathname.includes(RUTAS_PAGINAS.LOGIN)) {
        navigate(RUTAS_PAGINAS.INICIO)
      }
      setIsReadyToRender(true)
    } else {
      // Si el usuario no está autenticado, redirigir a la página de login si es que esta en una ruta protegida
      if (RUTAS_DESPROTEGIDAS.includes(pathname)) {
        setIsReadyToRender(true)
        return
      }
      navigate(RUTAS_PAGINAS.LOGIN)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [auth, location, navigate, loading])

  if (!isReadyToRender) {
    return (
      <div
        style={{
          width: '300px',
          height: '300px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto'
        }}
      >
        <Spinner />
      </div>
    )
  }

  return <>{children}</>
}

export default ProtectedRoute
