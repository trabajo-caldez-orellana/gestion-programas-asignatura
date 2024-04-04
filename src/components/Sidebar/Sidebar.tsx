import './Sidebar.css'
import SidebarSectionList from './SidebarSectionList'
import useAuth from '../../hooks/useAuth'

export default function Sidebar() {
  const { auth } = useAuth()

  return (
    <>
      <section className="sidebar-header">
        <h1>
          {auth.userFirstName} {auth.userLastName}
        </h1>
      </section>
      <section>
        <SidebarSectionList />
      </section>
    </>
  )
}
