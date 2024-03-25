import './Pendientes.css'
import useTareasPendientes from './hooks/useTareasPendientes'
import { Tabla } from './components'
import { Titulo } from '../../components'

export default function TareasPendientes() {
  const { loading, error } = useTareasPendientes()

  if (error) return <h1>Error</h1>

  if (loading) return <h1>Cargando...</h1>

  return (
    <div className="section-content">
      <Titulo>Tareas Pendientes</Titulo>
      <Tabla />
    </div>
  )
}
