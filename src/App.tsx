import { useState, useEffect } from 'react'
import './App.css'
import Navbar from './components/Navbar/Navbar'
import { Routes, Route } from 'react-router-dom'
import ProgramasAsignaturas from './pages/ProgramasAsignaturas'
import ProgramasVigentes from './pages/ProgramasVigentes'
import ProgramaAsignatura from './pages/ProgramasAsignaturas/components/ProgramaAsignatura'
import useProfile from './hooks/useProfile'
import useGoogleAuthLink from './hooks/useGoogleAuthLink'
import useGoogleAuthToken from './hooks/useGoogleAuthToken'
import { MODOS_PROGRAMA_ASIGNATURA } from './constants/constants'

export default function App() {
  // TODO: Empujar el contenido del main hacia la izquierda si se abre el sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const { data: profile, refetch: fetchProfile } = useProfile()
  const { data: googleAuth, refetch: fetchGoogleAuth } = useGoogleAuthLink()
  const { mutate, isSuccess } = useGoogleAuthToken()

  useEffect(() => {
    const searchParams = new URLSearchParams(document.location.search)

    const code = searchParams.get('code')
    const state = searchParams.get('state')

    if (code && state) {
      mutate({ code, state })
    }
  }, [mutate])

  useEffect(() => {
    if (isSuccess) {
      fetchProfile()
    }
  }, [isSuccess, fetchProfile])

  useEffect(() => {
    if (googleAuth) {
      window.location.replace(googleAuth.authorizationUrl)
    }
  }, [googleAuth])

  // Handlers
  const handleGoogleLogin = () => {
    fetchGoogleAuth()
  }

  const handleLogout = () => {
    localStorage.removeItem('token') // Remueve el token

    // Redirecciona a la página principal
    // TODO: Cambiar por la página de login
    // TODO: Implementar en el backend
    window.location.href = '/'
  }

  // TODO: Poner en otro archivo y crear archivo de constantes
  // const routes = {
  //   semestres: {
  //     path: '/semestres',
  //     element: <h1>Semestres</h1>
  //   },
  //   parametros: {
  //     path: '/parametros',
  //     element: <h1>Parametros</h1>
  //   },
  //   estandar: {
  //     path: '/estandar',
  //     element: <h1>Estandares</h1>
  //   },
  //   usuarios: {
  //     path: '/usuarios',
  //     element: <h1>Usuarios</h1>
  //   },
  //   carrera: {
  //     path: '/carrera',
  //     element: <h1>Carrera</h1>
  //   },
  //   planEstudio: {
  //     path: '/plan-estudio',
  //     element: <h1>Plan de Estudio</h1>
  //   },
  //   descriptores: {
  //     path: '/descriptores',
  //     element: <h1>Descriptores</h1>
  //   },
  //   bloqueCurricular: {
  //     path: '/bloque-curricular',
  //     element: <h1>Bloque curricular</h1>
  //   },
  //   programaAsignaturas: {
  //     path: '/programa-asignaturas',
  //     element: <ProgramasAsignaturas />
  //   },
  //   auditoria: {
  //     path: '/auditoria',
  //     element: <h1>Auditoria</h1>
  //   }
  // }

  return (
    <>
      <Navbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        profile={profile}
        handleLogin={handleGoogleLogin}
        handleLogout={handleLogout}
      />
      <main className={`main-content ${isSidebarOpen ? 'sidebar-active' : ''}`}>
        {/* TODO: Crear componente rutas */}
        <Routes>
          <Route
            path="/"
            element={
              <div className="App">
                {profile ? <h1>Bienvenido {profile.firstName}! :D</h1> : <></>}
              </div>
            }
          />
          <Route path="/carrera" element={<h1>Carrera</h1>} />
          <Route path="/plan-estudio" element={<h1>Plan de Estudio</h1>} />
          <Route path="/descriptores" element={<h1>Descriptores</h1>} />
          <Route
            path="/bloque-curricular"
            element={<h1>Bloque curricular</h1>}
          />
          <Route path="/programas-vigentes" element={<ProgramasVigentes />} />
          <Route
            path="/programa-asignaturas"
            element={<ProgramasAsignaturas />}
          />
          <Route
            path="/programa-asignaturas/:id"
            element={
              <ProgramaAsignatura modo={MODOS_PROGRAMA_ASIGNATURA.VER} />
            }
          />
          <Route
            path="/programa-asignaturas/editar/:id"
            element={
              <ProgramaAsignatura modo={MODOS_PROGRAMA_ASIGNATURA.EDITAR} />
            }
          />
          <Route
            path="/programa-asignaturas/nuevo/:id"
            element={
              <ProgramaAsignatura modo={MODOS_PROGRAMA_ASIGNATURA.NUEVO} />
            }
          />
          <Route path="/auditoria" element={<h1>Auditoria</h1>} />
          <Route path="*" element={<h1>Not found</h1>} />
        </Routes>
      </main>
    </>
  )
}
