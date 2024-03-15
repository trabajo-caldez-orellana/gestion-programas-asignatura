import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'

import { Navbar, ProtectedRoute } from './components'
import useGoogleAuthLink from './hooks/useGoogleAuthLink'
import useGoogleAuthToken from './hooks/useGoogleAuthToken'
import { PAGINAS } from './constants/constants'

export default function App() {
  // TODO: Empujar el contenido del main hacia la izquierda si se abre el sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const { data: googleAuth } = useGoogleAuthLink()
  const { mutate } = useGoogleAuthToken()

  useEffect(() => {
    const searchParams = new URLSearchParams(document.location.search)

    const code = searchParams.get('code')
    const state = searchParams.get('state')

    if (code && state) {
      mutate({ code, state })
    }
  }, [mutate])

  useEffect(() => {
    if (googleAuth) {
      window.location.replace(googleAuth.authorizationUrl)
    }
  }, [googleAuth])

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
        handleLogout={handleLogout}
      />
      <main className="main-content">
        <ProtectedRoute>
          <Routes>
            {PAGINAS.map((pagina) => (
              <Route
                key={pagina.key}
                path={pagina.path}
                element={
                  pagina.modo ? (
                    <pagina.component modo={pagina.modo} />
                  ) : (
                    <pagina.component />
                  )
                }
              />
            ))}
            <Route path="*" element={<h1>Not found</h1>} />
          </Routes>
        </ProtectedRoute>
      </main>
    </>
  )
}
