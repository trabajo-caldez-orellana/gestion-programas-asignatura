// import { useParams } from 'react-router-dom'
import { useState } from 'react'
import CargaHoraria from './CargaHoraria'
import InformacionAdicional from './InformacionAdicional'
import SeccionDescriptores from './SeccionDescriptores'
import { ProgramaAsignatura } from '../../../interfaces'

export default function ProgramaAsignatura() {
  //const { id } = useParams()
  const [programaAsignatura, setProgramaAsignatura] =
    useState<ProgramaAsignatura>({
      id: 1,
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
      },
      descriptores: {
        resultadosAprendizaje: [''],
        ejesTransversales: [
          {
            id: 1,
            nombre: 'Eje 1',
            valor: 0
          },

          {
            id: 2,
            nombre: 'Eje 2',
            valor: 2
          }
        ],
        descriptores: {
          si: [
            { id: 1, nombre: 'Descriptor 1' },
            { id: 2, nombre: 'Descriptor 2' }
          ],
          no: [{ id: 3, nombre: 'Descriptor 3' }]
        },
        actividadesReservadas: []
      },
      informacionAdicional: {
        fundamentacion: '',
        contenidos: '',
        bibliografia: '',
        metodologiaAplicada: '',
        recursos: '',
        evaluacion: '',
        investigacion: '',
        extension: ''
      }
    })

  return (
    <section className="section-content">
      <h1>Programa Asignatura</h1>
      <CargaHoraria
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
      />
      <SeccionDescriptores
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
      />
      <InformacionAdicional
        programaAsignatura={programaAsignatura}
        setProgramaAsignatura={setProgramaAsignatura}
      />
    </section>
  )
}
