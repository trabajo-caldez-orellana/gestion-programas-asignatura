import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'

import { Navbar, ProtectedRoute } from './components'
import { PAGINAS } from './constants/constants'
import { AuthProvider } from './context/authProvider'
import Cookies from 'js-cookie';

export default function App() {
  // TODO: Empujar el contenido del main hacia la izquierda si se abre el sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const handleLogout = () => {
    Cookies.remove('token'); // Remueve el token
    Cookies.remove('refresh_token'); // Remueve el token

    window.location.href = '/login'
  }

  return (
    <AuthProvider>
      <Navbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        handleLogout={handleLogout}
      />
      <main className="main-content">
        {/* <ProtectedRoute> */}
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
        {/* </ProtectedRoute> */}
      </main>
    </AuthProvider>
  )
}
