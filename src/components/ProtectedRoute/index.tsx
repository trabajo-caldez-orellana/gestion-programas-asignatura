import { PropsWithChildren, useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

import { RUTAS_PAGINAS } from '../../constants/constants'
import useAuth from '../../hooks/useAuth'

const RUTAS_DESPROTEGIDAS = [RUTAS_PAGINAS.LOGIN]

const ProtectedRoute: React.FC<PropsWithChildren> = ({ children }) => {

  const { auth } = useAuth()

  const navigate = useNavigate()
  const location = useLocation()

  const [isReadyToRender, setIsReadyToRender] = useState<boolean>(false)

  useEffect(() => {
    const pathname = location.pathname
    // if (isLoading) {
    //   setIsReadyToRender(false)
    //   return
    // }

    if (!auth.isLoggedIn) {
      if (RUTAS_DESPROTEGIDAS.includes(pathname)) {
        setIsReadyToRender(true)
        return
      }
      navigate(RUTAS_PAGINAS.LOGIN)
    } else {
      if (pathname.includes(RUTAS_PAGINAS.LOGIN)) {
        navigate(RUTAS_PAGINAS.INICIO)
      }
    }
    setIsReadyToRender(true)
  }, [auth, location, navigate])

  if (!isReadyToRender) {
    return <div>LOADING</div>
  }

  return <>{children}</>
}

export default ProtectedRoute
