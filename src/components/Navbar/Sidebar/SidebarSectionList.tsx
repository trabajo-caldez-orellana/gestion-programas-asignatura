import { useNavigate } from 'react-router-dom'
import {
  ROLES,
  SIDEBAR_SECTIONS,
  SidebarSection
} from '../../../constants/constants'
import useAuth from '../../../hooks/useAuth'
import { useEffect, useState } from 'react'
import {
  SectionContainer,
  SectionTitle,
  Title,
  SubsectionList,
  SubsectionItem,
  BotonSeccion
} from '../NavbarStyled'

interface SectionProps {
  onLinkClick: () => void
}

const SidebarSectionList: React.FC<SectionProps> = ({ onLinkClick }) => {
  const { auth } = useAuth()
  const navigate = useNavigate()
  const [seccionesFiltradas, setSeccionesFiltradas] = useState<
    SidebarSection[]
  >([])

  useEffect(() => {
    const secciones = SIDEBAR_SECTIONS.filter((seccion) => {
      const subseccionesFiltradas = seccion.sections.filter((subsection) => {
        if (
          subsection.permisos === null ||
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

  const handleLinkRedirect = (navigateTo: string) => {
    navigate(navigateTo)
    onLinkClick()
  }

  return (
    <>
      {seccionesFiltradas.map((section) => {
        return (
          <SectionContainer key={section.id}>
            <SectionTitle>
              <Title>{section.name}</Title>
            </SectionTitle>
            <SubsectionList>
              {section.sections.map((subsection) => {
                if (
                  subsection.permisos === null ||
                  auth.userRoles.es_administrador ||
                  (auth.userRoles.es_director_de_carrera &&
                    subsection.permisos.includes(ROLES.DOCENTE)) ||
                  (auth.userRoles.es_docente &&
                    subsection.permisos.includes(ROLES.DOCENTE)) ||
                  (auth.userRoles.es_secretario_academico &&
                    subsection.permisos.includes(ROLES.SECRETARIO))
                ) {
                  return (
                    <SubsectionItem key={subsection.id}>
                      <BotonSeccion
                        onClick={() => handleLinkRedirect(subsection.url)}
                      >
                        {subsection.name}
                      </BotonSeccion>
                    </SubsectionItem>
                  )
                }
              })}
            </SubsectionList>
          </SectionContainer>
        )
      })}
    </>
  )
}

export default SidebarSectionList
