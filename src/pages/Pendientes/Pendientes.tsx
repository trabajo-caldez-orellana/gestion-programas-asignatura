import './Pendientes.css'
import { Tabla } from './components'
import { Titulo } from '../../components'

export default function TareasPendientes() {
  return (
    <div className="section-content">
      <Titulo>Tareas Pendientes</Titulo>
      <Tabla />
    </div>
  )
}
