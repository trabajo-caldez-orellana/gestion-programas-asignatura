import './Navbar.css'
import Sidebar from '../Sidebar/Sidebar'
import Button from '../ui/Button'
import { useNavigate } from 'react-router-dom'

import useAuth from '../../hooks/useAuth'
import { RUTAS_PAGINAS } from '../../constants/constants'

interface NavbarProps {
  isSidebarOpen: boolean
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
}

export default function Navbar({
  isSidebarOpen,
  setIsSidebarOpen
}: NavbarProps) {
  const { auth, handleLogout } = useAuth()
  const navigate = useNavigate()

  const handleOpenSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState)
  }

  const handleLoginButton = () => {
    navigate(RUTAS_PAGINAS.LOGIN)
  }

  return (
    <nav className={`navbar wrapper ${isSidebarOpen ? '' : 'inactive'}`}>
      {auth.isLoggedIn && (
        <div className="section">
          <div className="top_navbar">
            <div className="hamburger">
              <a href="#" onClick={handleOpenSidebar}>
                <i className="fas fa-bars"></i>
              </a>
            </div>
          </div>
        </div>
      )}
      <ul id="navbar-items">
        {auth.isLoggedIn ? (
          <>
            <li>
              <Button text="Cerrar Sesión" onClick={handleLogout} />
            </li>
          </>
        ) : (
          <>
            <li>
              <Button text="Iniciar Sesión" onClick={handleLoginButton} />
            </li>
          </>
        )}
      </ul>
      {auth.isLoggedIn && (
        <div className="sidebar">
          <Sidebar />
        </div>
      )}
    </nav>
  )
}
