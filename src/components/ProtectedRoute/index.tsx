import { PropsWithChildren, useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

import { RUTAS_PAGINAS } from '../../constants/constants'
import useProfile from '../../hooks/useProfile'

const RUTAS_DESPROTEGIDAS = [RUTAS_PAGINAS.INICIO, RUTAS_PAGINAS.LOGIN]

const ProtectedRoute: React.FC<PropsWithChildren> = ({ children }) => {
  const { profileData, isLoading } = useProfile()

  const navigate = useNavigate()
  const location = useLocation()

  const [isReadyToRender, setIsReadyToRender] = useState<boolean>(false)

  useEffect(() => {
    const pathname = location.pathname
    if (RUTAS_DESPROTEGIDAS.includes(pathname)) {
      setIsReadyToRender(true)
      return
    }

    if (isLoading) {
      setIsReadyToRender(false)
      return
    }

    setIsReadyToRender(true)
    if (!profileData) {
      navigate(RUTAS_PAGINAS.LOGIN)
    }
  }, [profileData, location, isLoading])

  if (!isReadyToRender) {
    return <div>LOADING</div>
  }

  return <>{children}</>
}

export default ProtectedRoute
