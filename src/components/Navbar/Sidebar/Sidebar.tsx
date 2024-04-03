import SidebarSectionList from './SidebarSectionList'
import useAuth from '../../../hooks/useAuth'
import {
  SidebarListContainer,
  UserInfoSection,
  UserCardContainer,
  ProfilePicture
} from '../NavbarStyled'

interface SidebarProps {
  onLinkClick: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ onLinkClick }) => {
  const { auth } = useAuth()

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
    </SidebarListContainer>
  )
}

export default Sidebar
