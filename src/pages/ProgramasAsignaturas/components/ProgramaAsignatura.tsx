// import { useParams } from 'react-router-dom'
import { useState } from 'react'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'

type CargaHorariaType = {
  cargaHorariaTotal: number
  semanasDictado: number
  teoriaPresencial: number
  practicaPresencial: number
  teoricoPracticoPresencial: number
  laboratoriosPresenciales: number
  teoriaDistancia: number
  practicaDistancia: number
  teoricoPracticoDistancia: number
  laboratorioDistancia: number
}

type DescriptorType = {
  resultadosAprendizaje: string[]
  ejesTransversales: {
    nombre: string
    valor: number
  }[]
  descriptores: {
    si: { id: number; nombre: string }[]
    no: { id: number; nombre: string }[]
  }
  actividadesReservadas: string[]
}




type ProgramaAsignaturaType = {
  cargaHoraria: CargaHorariaType
}

export default function ProgramaAsignatura() {
  //const { id } = useParams()
  const [programaAsignatura, setProgramaAsignatura] =
    useState<ProgramaAsignaturaType>({
      cargaHoraria: {
        cargaHorariaTotal: 0,
        semanasDictado: 0,
        teoriaPresencial: 0,
        practicaPresencial: 0,
        teoricoPracticoPresencial: 0,
        laboratoriosPresenciales: 0,
        teoriaDistancia: 0,
        practicaDistancia: 0,
        teoricoPracticoDistancia: 0,
        laboratorioDistancia: 0
      }
    })

  return (
    <section className="section-content">
      <h1>ProgramaAsignatura</h1>
      <CargaHoraria />
      <SeccionDescriptores />
      <InformacionAdicional />
    </section>
  )
}
