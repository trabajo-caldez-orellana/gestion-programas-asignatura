import { rest } from 'msw'

// TODO: crear un archivo para cada mock response
const handlers = [
  rest.get('/programa-asignaturas/:id', (_, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.delay(1000),
      ctx.json({
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
    )
  })
]

export default handlers
