import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import './App.css'

import { Navbar, ProtectedRoute } from './components'
import { PAGINAS } from './constants/constants'
import { AuthProvider } from './context/authProvider'
import { MainContentContainer } from './components'

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <AuthProvider>
      <ProtectedRoute>
        <Navbar
          isSidebarOpen={isSidebarOpen}
          setIsSidebarOpen={setIsSidebarOpen}
        />
        <MainContentContainer>
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
        </MainContentContainer>
      </ProtectedRoute>
    </AuthProvider>
  )
}
