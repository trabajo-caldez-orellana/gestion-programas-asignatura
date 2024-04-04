import Button from '../../components/ui/Button'
import { RUTAS_PAGINAS } from '../../constants/constants'
import { useNavigate } from 'react-router-dom'
import useAuth from '../../hooks/useAuth'
import {
  Division,
  Funcionalidad,
  Portada,
  SeccionFuncionalidades,
  TituloFuncionalidad,
  IconoFuncionalidad,
  DescripcionFuncionalidad,
  TextoBienvenidaContainer,
  LogoFacet
} from './InicioStyled'
import img from '../../img'

const Inicio: React.FC = () => {
  const { auth } = useAuth()
  const navigate = useNavigate()

  const handleLoginButton = () => {
    navigate(RUTAS_PAGINAS.LOGIN)
  }

  return (
    <>
      <Portada>
        <TextoBienvenidaContainer>
          <TituloFuncionalidad>
            <b>¡Bienvenido a SGPA!</b>
          </TituloFuncionalidad>
          <DescripcionFuncionalidad>
            <b>Sistema de Gestion para Programas de Asignautra</b> para la
            Facultad de Ciencias Exactas y Tecnología de la Universidad Nacional
            de Tucumán.
            <br />
            <br />
            {auth.isLoggedIn ? (
              <>
                Contáctese con el administrador del sistema para obtener los
                permisos necesarios para utilizar el sistema, si aún no los
                tiene.
              </>
            ) : (
              <>
                Inicie sesión para acceder a las funcionalidades del sistema.
                <br />
                <Button text="Iniciar Sesión" onClick={handleLoginButton} />
              </>
            )}
          </DescripcionFuncionalidad>
        </TextoBienvenidaContainer>
        <LogoFacet src={img.FACETNoBackground} />
      </Portada>
      <Division>Explore las funcionalidades del Sistema</Division>
      <SeccionFuncionalidades>
        <Funcionalidad>
          <IconoFuncionalidad>
            <i className="fas fa-regular fa-file" />
          </IconoFuncionalidad>
          <TituloFuncionalidad>Generación de informes</TituloFuncionalidad>
          <DescripcionFuncionalidad>
            Permite generar informes sobre las distintas asignaturas de cada
            carrera, por ejemplo, generación de la matriz de tributación.
          </DescripcionFuncionalidad>
        </Funcionalidad>
        <Funcionalidad>
          <IconoFuncionalidad>
            <i className="fas fa-regular fa-clock" />
          </IconoFuncionalidad>
          <TituloFuncionalidad>historial de programas</TituloFuncionalidad>
          <DescripcionFuncionalidad>
            Filtrar, y buscar programas de asignaturas de distintos semestres y
            años lectivos. También descargar los programas en PDF.
          </DescripcionFuncionalidad>
        </Funcionalidad>
        <Funcionalidad>
          <IconoFuncionalidad>
            <i className="fas fa-solid fa-pen" />
          </IconoFuncionalidad>
          <TituloFuncionalidad>actualización de programas</TituloFuncionalidad>
          <DescripcionFuncionalidad>
            Permite a los docentes actualizar los programas de asignatura para
            cada semestre de cursado, y a directores de carrera validar los
            cambios.
          </DescripcionFuncionalidad>
        </Funcionalidad>
      </SeccionFuncionalidades>
    </>
  )
}

export default Inicio
