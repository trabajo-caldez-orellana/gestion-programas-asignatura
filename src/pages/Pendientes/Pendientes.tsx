import './Pendientes.css'
import useTareasPendientes from './hooks/useTareasPendientes'
import { Tabla } from './components'

export default function TareasPendientes() {
  const { loading, error } = useTareasPendientes()

  if (error) return <h1>Error</h1>

  if (loading) return <h1>Cargando...</h1>

  return (
    <div className="section-content">
      <h1 className="header">Tareas Pendientes</h1>
      <Tabla />
    </div>
  )
}
