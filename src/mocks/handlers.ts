import { rest } from 'msw'
import programasAsignaturas from './fixtures/programasAsignaturas.json'
import { HANDLERS } from '../constants/constants'

// TODO: crear un archivo para cada mock response
const handlers = [
  rest.get(HANDLERS.GET_PROGRAMA_ASIGNATURA_HANDLER, (_, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.delay(1000),
      ctx.json(programasAsignaturas)
    )
  })
]

export default handlers
