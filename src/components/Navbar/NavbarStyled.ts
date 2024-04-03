import styled from 'styled-components'

interface NavbarProps {
  $isOpen: boolean
}

export const NavbarWrapper = styled.nav<NavbarProps>`
  background-color: var(--dark-color);
  border-bottom: 1px solid var(--contrast-color);
  box-shadow: 0 1px 2px var(--dark-color);
  width: 100%;
  display: flex;
  align-items: center;
  gap: 2rem;
  position: relative;
`

export const BurgerButton = styled.button<NavbarProps>`
  left: ${(p) => (p.$isOpen ? '350px' : '0')};
  position: absolute;
  transition: 0.5s ease-in-out;
  margin: 0 10px;
  color: white;
  border: none;
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
  background-color: var(--primary-color);
  width: 350px;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);

  left: ${(p) => (p.$isOpen ? '0' : '-350px')};
  transition: 0.5s ease-in-out;
`

export const ButtonList = styled.ul`
  position: relative;
  margin: 0 10px 0 auto;
  list-style: none;
`
