import {
  NavbarWrapper,
  SidebarContainer,
  BurgerButton,
  ContentOverlay
} from './NavbarStyled'
import Sidebar from './Sidebar/Sidebar'
import { useRef, useEffect } from 'react'
import useAuth from '../../hooks/useAuth'

interface NavbarProps {
  isSidebarOpen: boolean
  setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
}

export default function Navbar({
  isSidebarOpen,
  setIsSidebarOpen
}: NavbarProps) {
  const { auth } = useAuth()

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
      {auth.isLoggedIn && (
        <SidebarContainer $isOpen={isSidebarOpen} ref={sidebarRef}>
          <Sidebar onLinkClick={onLinkClick} />
        </SidebarContainer>
      )}
    </NavbarWrapper>
  )
}
