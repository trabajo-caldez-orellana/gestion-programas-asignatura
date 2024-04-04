import SidebarSectionList from './SidebarSectionList'
import useAuth from '../../../hooks/useAuth'

import {
  SidebarListContainer,
  UserInfoSection,
  UserCardContainer,
  ProfilePicture,
  BotonSeccion
} from '../NavbarStyled'

interface SidebarProps {
  onLinkClick: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ onLinkClick }) => {
  const { auth, handleLogout } = useAuth()

  const handleClickLogoutButton = () => {
    onLinkClick()
    handleLogout()
  }

  return (
    <SidebarListContainer>
      <UserInfoSection>
        <UserCardContainer>
          <ProfilePicture src={auth.userProfilePicture || ''} />
          <p>
            {auth.userFirstName} {auth.userLastName}
          </p>
        </UserCardContainer>
      </UserInfoSection>
      <SidebarSectionList onLinkClick={onLinkClick} />

      <BotonSeccion className="cerrar-sesion" onClick={handleClickLogoutButton}>
        Cerrar Sesión
      </BotonSeccion>
    </SidebarListContainer>
  )
}

export default Sidebar
