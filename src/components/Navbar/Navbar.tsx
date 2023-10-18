import './Navbar.css'
import Sidebar from '../Sidebar/Sidebar'
import Button from '../ui/Button'
import { Profile } from '../../api/types.ts'

interface NavbarProps {
  isSidebarOpen: boolean
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
  isLogged: Profile | undefined
  handleLogin: () => void
  handleLogout: () => void
}

export default function Navbar({
  isSidebarOpen,
  setIsSidebarOpen,
  isLogged,
  handleLogin,
  handleLogout
}: NavbarProps) {
  const handleOpenSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState)
  }

  return (
    <>
      <nav className={`navbar wrapper ${isSidebarOpen ? '' : 'inactive'}`}>
        <div className="section">
          <div className="top_navbar">
            <div className="hamburger">
              <a href="#" onClick={handleOpenSidebar}>
                <i className="fas fa-bars"></i>
              </a>
            </div>
          </div>
        </div>
        <ul id="navbar-items">
          <li>
            <Button text="Notificaciones" />
          </li>
          <li>
            <Button text="Nuevo usuario" />
          </li>
          {isLogged ? (
            <li>
              <Button text="Cerrar Sesion" onClick={handleLogout} />
            </li>
          ) : (
            <li>
              <Button text="Iniciar Sesion" onClick={handleLogin} />
            </li>
          )}
        </ul>
        <div className="sidebar">
          <Sidebar
            userinfo={{ name: 'Gonzalo Orellana', email: 'ore@gmail.com' }}
          />
        </div>
      </nav>
    </>
  )
}
