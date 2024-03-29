import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'

import { Navbar, ProtectedRoute } from './components'
import { PAGINAS } from './constants/constants'
import { AuthProvider } from './context/authProvider'

export default function App() {
  // TODO: Empujar el contenido del main hacia la izquierda si se abre el sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  console.log('PAGINAS', PAGINAS)
  return (
    <AuthProvider>
      <Navbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
      />
      <main className={`main-content ${isSidebarOpen ? 'sidebar-active' : ''}`}>
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
