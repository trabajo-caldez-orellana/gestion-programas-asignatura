import styled from 'styled-components'

interface NavbarProps {
  $isOpen: boolean
}

export const NavbarWrapper = styled.nav<NavbarProps>`
  background-color: var(--dark-color);
  border-bottom: 1px solid var(--dark-color);
  width: 100%;
  display: flex;
  align-items: center;
  gap: 2rem;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 50px;

  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const BurgerButton = styled.button<NavbarProps>`
  left: ${(p) => (p.$isOpen ? '350px' : '0')};
  position: absolute;
  transition: 0.5s ease-in-out;
  margin: 0 10px;
  color: white;
  border: none;
  font-size: 20px;
  background-color: transparent;

  a:visited {
    color: white;
  }
`

export const SidebarContainer = styled.div<NavbarProps>`
  position: absolute;
  top: 0;
  bottom: 0;
  height: 100vh;
  z-index: 20;
  background-color: var(--primary-color);
  width: 350px;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);

  left: ${(p) => (p.$isOpen ? '0' : '-350px')};
  opacity: ${(p) => (p.$isOpen ? '1' : '0')};
  transition: 0.5s ease-in-out;
`

export const ButtonList = styled.ul`
  position: relative;
  margin: 0 10px 0 auto;
  list-style: none;
`

export const UserInfoSection = styled.div`
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: flex-start;

  box-sizing: border-box;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const UserCardContainer = styled.div`
  color: white;
  font-size: 20px;
  font-weight: 700;
  text-transform: uppercase;
  margin-left: 20px;
`

export const SidebarListContainer = styled.div`
  width: 100%;
`

export const ContentOverlay = styled.div<NavbarProps>`
  background-color: ${(p) => (p.$isOpen ? '#00000022' : 'transparent')};
  height: calc(100vh - 50px);
  width: 100vw;
  z-index: 10;
  transition: 0.5s ease-in-out;
  position: absolute;
  top: 50px;
`
