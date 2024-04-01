import './Sidebar.css'
import SidebarSectionList from './SidebarSectionList'

interface SidebarProps {
  userinfo: {
    name: string
    email: string | null
  }
}

export default function Sidebar({ userinfo }: SidebarProps) {
  return (
    <>
      <section className="sidebar-header">
        <h1>{userinfo.name} </h1>
      </section>
      <section>
        <SidebarSectionList />
      </section>
    </>
  )
}
