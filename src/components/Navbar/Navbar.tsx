import './Navbar.css'
import Sidebar from '../Sidebar/Sidebar'
import Button from '../ui/Button'
import { useEffect, useState } from 'react'

import useProfile from '../../hooks/useProfile.ts'

interface NavbarProps {
  isSidebarOpen: boolean
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
  handleLogin: () => void
  handleLogout: () => void
}

export default function Navbar({
  isSidebarOpen,
  setIsSidebarOpen,
  handleLogin,
  handleLogout
}: NavbarProps) {
  const { profileData, isLoading } = useProfile()
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)

  const handleOpenSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState)
  }

  useEffect(() => {
    setIsAuthenticated(!isLoading && !!profileData)
  }, [profileData, isLoading])

  return (
    <>
      <nav className={`navbar wrapper ${isSidebarOpen ? '' : 'inactive'}`}>
        <div className="section">
          <div className="top_navbar">
            {isAuthenticated ? (
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
          {isAuthenticated ? (
            <>
              <li>
                <Button text="Cerrar Sesion" onClick={handleLogout} />
              </li>
              <li>
                <Button text="Notificaciones" />
              </li>
            </>
          ) : (
            <li>
              <Button text="Iniciar Sesion" onClick={handleLogin} />
            </li>
          )}
        </ul>
        <div className="sidebar">
          {profileData ? (
            <Sidebar
              userinfo={{
                name: `${profileData.firstName} ${profileData.lastName}`,
                email: profileData.email
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
