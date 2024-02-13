import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'

import { Navbar } from './components'
import {
  Historial,
  TareasPendientes,
  ProgramaAsignatura,
  ProgramasVigentes
} from './pages'
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
      // fetchProfile()
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
          <Route path="/programa-asignaturas" element={<Historial />} />

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
          <Route
            path="/programa-asignaturas/editar-ultimo/:id"
            element={
              <ProgramaAsignatura
                modo={MODOS_PROGRAMA_ASIGNATURA.EDITAR_ULTIMO}
              />
            }
          />
          <Route path="/tareas-pendientes" element={<TareasPendientes />} />
          <Route path="/historial" element={<Historial />} />
          <Route path="/auditoria" element={<h1>Auditoria</h1>} />
          <Route path="*" element={<h1>Not found</h1>} />
        </Routes>
      </main>
    </>
  )
}
