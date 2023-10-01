import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar/Navbar'
import { Routes, Route } from 'react-router-dom'
import ProgramasAsignaturas from './pages/ProgramasAsignaturas'
import ProgramaAsignatura from './pages/ProgramasAsignaturas/components/ProgramaAsignatura'

function App() {
  // TODO: Empujar el contenido del main hacia la izquierda si se abre el sidebar
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  return (
    <>
      <Navbar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
      />
      <main className={`main-content ${isSidebarOpen ? 'sidebar-active' : ''}`}>
        <Routes>
          <Route path="/" element={<h1>Home</h1>} />
          <Route path="/semestres" element={<h1>Semestres</h1>} />
          <Route path="/parametros" element={<h1>Parametros</h1>} />
          <Route path="/estandar" element={<h1>Estandares</h1>} />
          <Route path="/usuarios" element={<h1>Usuarios</h1>} />
          <Route path="/carrera" element={<h1>Carrera</h1>} />
          <Route path="/plan-estudio" element={<h1>Plan de Estudio</h1>} />
          <Route path="/descriptores" element={<h1>Descriptores</h1>} />
          <Route
            path="/bloque-curricular"
            element={<h1>Bloque curricular</h1>}
          />
          <Route
            path="/programa-asignaturas"
            element={<ProgramasAsignaturas />}
          />
          <Route
            path="/programa-asignaturas/:id"
            element={<ProgramaAsignatura />}
          />
          <Route path="/auditoria" element={<h1>Auditoria</h1>} />
          <Route path="*" element={<h1>Not found</h1>} />
        </Routes>
      </main>
    </>
  )
}

export default App
