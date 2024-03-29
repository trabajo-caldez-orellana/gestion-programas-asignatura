import './Navbar.css'
import Sidebar from '../Sidebar/Sidebar'
import Button from '../ui/Button'
import { useEffect, useState } from 'react'

import useAuth from "../../hooks/useAuth";

interface NavbarProps {
  isSidebarOpen: boolean
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
  handleLogout: () => void
}

export default function Navbar({
  isSidebarOpen,
  setIsSidebarOpen,
  handleLogout
}: NavbarProps) {

  const { auth } = useAuth()

  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)

  const handleOpenSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState)
  }

  useEffect(() => {
    setIsAuthenticated(auth.isLoggedIn)
  }, [auth])

  return isAuthenticated ? (
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
          <>
            <li>
              <Button text="Cerrar Sesion" onClick={handleLogout} />
            </li>
            <li>
              <Button text="Notificaciones" />
            </li>
          </>
        </ul>
        <div className="sidebar">
          {auth.isLoggedIn ? (
            <Sidebar
              userinfo={{
                name: `${auth.userFirstName} ${auth.userLastName}`,
                email: auth.userEmail
              }}
            />
          ) : (
            <></>
          )}
        </div>
      </nav>
    </>
  ) : (
    <></>
  )
}
