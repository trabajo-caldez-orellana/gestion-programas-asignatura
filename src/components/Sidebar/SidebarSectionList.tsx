import './SidebarSectionList.css'
import { Link } from 'react-router-dom'

export default function SidebarSectionList() {
  type SidebarSection = {
    name: string
    sections: {
      name: string
      url: string
    }[]
  }

  const sidebarSection: SidebarSection[] = [
    {
      name: 'Administracion general',
      sections: [
        {
          name: 'Semestres',
          url: '/semestres'
        },
        {
          name: 'Parametros de Conf.',
          url: '/parametros'
        },
        {
          name: 'Estandar',
          url: '/estandar'
        },
        {
          name: 'Usuarios',
          url: '/usuarios'
        }
      ]
    },
    {
      name: 'Carrera',
      sections: [
        {
          name: 'Carrera',
          url: '/carrera'
        },
        {
          name: 'Plan de Estudio',
          url: '/plan-estudio'
        },
        {
          name: 'Descriptores',
          url: '/descriptores'
        }
      ]
    },
    {
      name: 'Asignaturas',
      sections: [
        {
          name: 'Bloque curricular',
          url: '/bloque-curricular'
        },
        {
          name: 'Programa de asignaturas',
          url: '/programa-asignaturas'
        },
        {
          name: 'Auditoria',
          url: '/auditoria'
        }
      ]
    }
  ]

  // TODO: Excluir si no tienen permisos

  return (
    <>
      {sidebarSection.map((section) => {
        return (
          <section>
            <section className="section-header">
              <h2>{section.name}</h2>
            </section>
            <ul className="sidebar-section-items">
              {section.sections.map((subsection) => {
                return (
                  <li>
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
