import './Sidebar.css'
import SidebarSectionList from './SidebarSectionList'

interface SidebarProps {
  userinfo: {
    name: string
    email: string
  }
}

export default function Sidebar({ userinfo }: SidebarProps) {
  return (
    <>
      <section className="sidebar-header">
        {/* TODO: DARLE EL MISMO HEIGH QUE EL NAVBAR */}
        <h1>{userinfo.name} </h1>
      </section>
      <section>
        <SidebarSectionList />
      </section>
    </>
  )
}
