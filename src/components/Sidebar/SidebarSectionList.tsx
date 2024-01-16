import './SidebarSectionList.css'
import { Link } from 'react-router-dom'
import { SIDEBAR_SECTIONS } from '../../constants/constants'

export default function SidebarSectionList() {
  // TODO: Excluir si no tienen permisos

  return (
    <>
      {SIDEBAR_SECTIONS.map((section) => {
        return (
          <section key={section.name}>
            <section className="section-header">
              <h2>{section.name}</h2>
            </section>
            <ul className="sidebar-section-items">
              {section.sections.map((subsection) => {
                return (
                  <li key={subsection.url}>
                    <div>
                      <Link to={subsection.url}>{subsection.name}</Link>
                    </div>
                  </li>
                )
              })}
            </ul>
          </section>
        )
      })}
    </>
  )
}
