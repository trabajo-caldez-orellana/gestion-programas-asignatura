import './SidebarSectionList.css'
import { Link } from 'react-router-dom'
import {
  ROLES,
  SIDEBAR_SECTIONS,
  SidebarSection
} from '../../constants/constants'
import useAuth from '../../hooks/useAuth'
import { useEffect, useState } from 'react'
export default function SidebarSectionList() {
  const { auth } = useAuth()
  const [seccionesFiltradas, setSeccionesFiltradas] = useState<
    SidebarSection[]
  >([])

  useEffect(() => {
    const secciones = SIDEBAR_SECTIONS.filter((seccion) => {
      const subseccionesFiltradas = seccion.sections.filter((subsection) => {
        if (
          auth.userRoles.es_administrador ||
          (auth.userRoles.es_director_de_carrera &&
            subsection.permisos.includes(ROLES.DOCENTE)) ||
          (auth.userRoles.es_docente &&
            subsection.permisos.includes(ROLES.DOCENTE)) ||
          (auth.userRoles.es_secretario_academico &&
            subsection.permisos.includes(ROLES.SECRETARIO))
        ) {
          return subsection
        }
      })

      if (subseccionesFiltradas.length > 0) {
        return {
          id: seccion.id,
          name: seccion.name,
          sections: subseccionesFiltradas
        }
      }
    })

    setSeccionesFiltradas(secciones)
  }, [auth])

  return (
    <>
      {seccionesFiltradas.map((section) => {
        return (
          <section key={section.id}>
            <section className="section-header">
              <h2>{section.name}</h2>
            </section>
            <ul className="sidebar-section-items">
              {section.sections.map((subsection) => {
                if (
                  auth.userRoles.es_administrador ||
                  (auth.userRoles.es_director_de_carrera &&
                    subsection.permisos.includes(ROLES.DOCENTE)) ||
                  (auth.userRoles.es_docente &&
                    subsection.permisos.includes(ROLES.DOCENTE)) ||
                  (auth.userRoles.es_secretario_academico &&
                    subsection.permisos.includes(ROLES.SECRETARIO))
                ) {
                  return (
                    <li key={subsection.id}>
                      <div>
                        <Link to={subsection.url}>{subsection.name}</Link>
                      </div>
                    </li>
                  )
                }
              })}
            </ul>
          </section>
        )
      })}
    </>
  )
}
