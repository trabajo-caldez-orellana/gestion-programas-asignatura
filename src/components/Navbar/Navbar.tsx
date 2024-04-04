import {
  NavbarWrapper,
  SidebarContainer,
  BurgerButton,
  ButtonList,
  ContentOverlay
} from './NavbarStyled'
import Sidebar from './Sidebar/Sidebar'
import Button from '../ui/Button'
import { useNavigate } from 'react-router-dom'
import { useRef, useEffect } from 'react'
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

  const sidebarRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        sidebarRef.current &&
        !sidebarRef.current.contains(event.target as Node)
      ) {
        setIsSidebarOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const handleOpenSidebar = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation()
    setIsSidebarOpen((state) => !state)
  }

  const handleLoginButton = () => {
    navigate(RUTAS_PAGINAS.LOGIN)
  }

  const onLinkClick = () => {
    setIsSidebarOpen(false)
  }

  return (
    <NavbarWrapper $isOpen={isSidebarOpen}>
      {isSidebarOpen && <ContentOverlay $isOpen={isSidebarOpen} />}
      {auth.isLoggedIn && (
        <BurgerButton
          $isOpen={isSidebarOpen}
          onClick={(event) => handleOpenSidebar(event)}
        >
          <i className="fas fa-bars"></i>
        </BurgerButton>
      )}
      <ButtonList>
        {auth.isLoggedIn ? (
          <li>
            <Button text="Cerrar Sesión" onClick={handleLogout} />
          </li>
        ) : (
          <li>
            <Button text="Iniciar Sesión" onClick={handleLoginButton} />
          </li>
        )}
      </ButtonList>
      {auth.isLoggedIn && (
        <SidebarContainer $isOpen={isSidebarOpen} ref={sidebarRef}>
          <Sidebar onLinkClick={onLinkClick} />
        </SidebarContainer>
      )}
    </NavbarWrapper>
  )
}
