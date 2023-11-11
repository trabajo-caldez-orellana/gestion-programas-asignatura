import { rest } from 'msw'
import programaAsignaturas from './fixtures/programaAsignaturas.json'
import programasAsignaturas from './fixtures/programasAsignaturas.json'
import { HANDLERS } from '../constants/constants'

const handlers = [
  rest.get(HANDLERS.GET_PROGRAMA_ASIGNATURA_HANDLER, (_, res, ctx) => {
    return res(ctx.status(200), ctx.delay(500), ctx.json(programaAsignaturas))
  }),
  rest.post(HANDLERS.POST_PROGRAMA_ASIGNATURA_HANDLER, (_, res, ctx) => {
    return res(ctx.status(200), ctx.delay(500), ctx.json({ success: true }))
  }),
  rest.get(HANDLERS.GET_PROGRAMAS_ASIGNATURAS_HANDLER, (_, res, ctx) => {
    return res(ctx.status(200), ctx.delay(500), ctx.json(programasAsignaturas))
  })
]

export default handlers
