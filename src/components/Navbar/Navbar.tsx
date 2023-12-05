import './Navbar.css'
import Sidebar from '../Sidebar/Sidebar'
import Button from '../ui/Button'
import { Profile } from '../../api/types.ts'

interface NavbarProps {
  isSidebarOpen: boolean
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
  profile: Profile | undefined
  handleLogin: () => void
  handleLogout: () => void
}

export default function Navbar({
  isSidebarOpen,
  setIsSidebarOpen,
  profile,
  handleLogin,
  handleLogout
}: NavbarProps) {
  const handleOpenSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState)
  }

  // Si tenemos un profile es porque estamos logueados

  return (
    <>
      <nav className={`navbar wrapper ${isSidebarOpen ? '' : 'inactive'}`}>
        <div className="section">
          <div className="top_navbar">
            {profile ? (
              <div className="hamburger">
                <a href="#" onClick={handleOpenSidebar}>
                  <i className="fas fa-bars"></i>
                </a>
              </div>
            ) : (
              <></>
            )}
          </div>
        </div>
        <ul id="navbar-items">
          <li>
            <Button text="Notificaciones" />
          </li>
          {profile ? (
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
          {profile ? (
            <Sidebar
              userinfo={{
                name: `${profile.firstName} ${profile.lastName}`,
                email: profile.email
              }}
            />
          ) : (
            <></>
          )}
        </div>
      </nav>
    </>
  )
}
