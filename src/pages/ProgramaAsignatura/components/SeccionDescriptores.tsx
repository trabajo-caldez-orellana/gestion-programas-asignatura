import {
  Formulario,
  TituloSeccion,
  SeleccionConModal,
  Button,
  DoubleSelectionInput
} from '../../../components'
import {
  ProgramaAsignaturaInterface,
  ProgramaAsignaturaErrores
} from '../../../interfaces/interfaces'
import {
  MODOS_PROGRAMA_ASIGNATURA,
  DatosListaSeleccionInterface
} from '../../../constants/constants'
import {
  InputOutsideContainer,
  SeccionFormulario,
  WholeWidthInputContainer
} from './SeccionFormulario'

interface SeccionDescriptoresProps {
  programaAsignatura: ProgramaAsignaturaInterface
  setProgramaAsignatura: (
    programaAsignatura: ProgramaAsignaturaInterface
  ) => void
  modoProgramaAsignatura: string
  erroresPrograma: ProgramaAsignaturaErrores
}

export default function SeccionDescriptores({
  programaAsignatura,
  setProgramaAsignatura,
  modoProgramaAsignatura,
  erroresPrograma
}: SeccionDescriptoresProps) {
  const { descriptores } = programaAsignatura
  const modoLectura =
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.VER ||
    modoProgramaAsignatura === MODOS_PROGRAMA_ASIGNATURA.REVISAR

  const datosListaSeleccionDescriptores: DatosListaSeleccionInterface[] =
    descriptores.descriptores.map((descriptor) => {
      return {
        id: descriptor.id,
        informacion: descriptor.nombre,
        seleccionado: descriptor.seleccionado
      }
    })

  const handleResultadosAprendizajeChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>,
    index: number
  ) => {
    const { value } = e.target

    const resultadosAprendizaje = [
      ...programaAsignatura.descriptores.resultadosAprendizaje
    ]
    resultadosAprendizaje[index] = value

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,
        resultadosAprendizaje: resultadosAprendizaje
      }
    })
  }

  const resultadosAprendizajeCount = () => {
    //Contar solo los resultados de aprendizaje que no sean string vacios
    const resultadosAprendizaje =
      programaAsignatura.descriptores.resultadosAprendizaje || []

    return resultadosAprendizaje.filter((item) => item !== '').length || 0
  }

  const aniadirResultadoAprendizaje = () => {
    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        resultadosAprendizaje: [
          ...programaAsignatura.descriptores.resultadosAprendizaje,
          ''
        ]
      }
    })
  }

  // Al abrir el modal limpiamos los resultados de aprendizaje que son string vacios
  const abrirModalResultados = () => {
    const resultadosAprendizaje: string[] =
      descriptores.resultadosAprendizaje || []
    const resultadosAprendizajeLimpios = resultadosAprendizaje.filter(
      (item) => item !== ''
    )
    if (resultadosAprendizajeLimpios.length === 0)
      resultadosAprendizajeLimpios.push('')

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        resultadosAprendizaje: resultadosAprendizajeLimpios
      }
    })
  }

  const handleEjeTransversalChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const { value } = e.target

    const ejesTransversales = [...descriptores.ejesTransversales]
    ejesTransversales[index].nivel = parseInt(value)

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        ejesTransversales
      }
    })
  }

  const handleDescriptorChange = (id: number) => {
    // Toggle the field seleccionado for the descriptor with the given id
    if (modoLectura) return
    const descriptores = [...programaAsignatura.descriptores.descriptores]
    const descriptor = descriptores.find((descriptor) => descriptor.id === id)
    if (descriptor) descriptor.seleccionado = !descriptor.seleccionado

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,

        descriptores
      }
    })
  }

  const handleActividadReservadaChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const { value } = e.target
    const actividadesReservadas = [...descriptores.actividadesReservadas]
    actividadesReservadas[index].nivel = parseInt(value)

    setProgramaAsignatura({
      ...programaAsignatura,
      descriptores: {
        ...programaAsignatura.descriptores,
        actividadesReservadas
      }
    })
  }

  return (
    <SeccionFormulario>
      <TituloSeccion>Información Específica</TituloSeccion>
      <Formulario>
        <InputOutsideContainer>
          <SeleccionConModal
            onOpenModal={abrirModalResultados}
            name="resultados-aprendizaje"
            valorInput={resultadosAprendizajeCount()}
            mensajeDeError={erroresPrograma.descriptores.resultadosAprendizaje}
            isDisabled={modoLectura}
            tituloModal="Resultados de Aprendizaje"
          >
            {descriptores.resultadosAprendizaje.map((resultado, index) => (
              <div key={index}>
                {/* {TODO: CREAR COMPONENTE} */}
                <textarea
                  key={index}
                  value={resultado}
                  onChange={(e) => handleResultadosAprendizajeChange(e, index)}
                  rows={4}
                  cols={50}
                  disabled={modoLectura}
                />
                {index === descriptores.resultadosAprendizaje.length - 1 && (
                  <div className="sumar-text-area">
                    <Button
                      text="+"
                      onClick={aniadirResultadoAprendizaje}
                      disabled={modoLectura}
                    ></Button>
                  </div>
                )}
              </div>
            ))}
          </SeleccionConModal>
        </InputOutsideContainer>
        <InputOutsideContainer>
          <SeleccionConModal
            name="ejes-transversales"
            valorInput={descriptores.ejesTransversales.length}
            mensajeDeError={erroresPrograma.descriptores.ejesTransversales}
            isDisabled={modoLectura}
            tituloModal="Ejes Transversales"
          >
            {descriptores.ejesTransversales.map((eje, index) => (
              <div key={index}>
                <label>{eje.nombre}</label>
                <div className="radio-buttons">
                  <input
                    type="radio"
                    name={eje.nombre}
                    value="0"
                    defaultChecked
                    checked={eje.nivel === 0}
                    onChange={(e) => handleEjeTransversalChange(e, index)}
                    disabled={modoLectura}
                  />
                  Nada
                  <input
                    type="radio"
                    name={eje.nombre}
                    value="1"
                    checked={eje.nivel === 1}
                    onChange={(e) => handleEjeTransversalChange(e, index)}
                    disabled={modoLectura}
                  />
                  Bajo
                  <input
                    type="radio"
                    name={eje.nombre}
                    value="2"
                    checked={eje.nivel === 2}
                    onChange={(e) => handleEjeTransversalChange(e, index)}
                    disabled={modoLectura}
                  />
                  Medio
                  <input
                    type="radio"
                    name={eje.nombre}
                    value="3"
                    checked={eje.nivel === 3}
                    onChange={(e) => handleEjeTransversalChange(e, index)}
                    disabled={modoLectura}
                  />
                  Alto
                </div>
              </div>
            ))}
          </SeleccionConModal>
        </InputOutsideContainer>
        <InputOutsideContainer>
          <SeleccionConModal
            name="actividades-reservadas"
            valorInput={descriptores.ejesTransversales.length}
            mensajeDeError={erroresPrograma.descriptores.ejesTransversales}
            isDisabled={modoLectura}
            tituloModal="Actividades Reservadas"
          >
            {descriptores.actividadesReservadas.map((actividad, index) => (
              <div key={index}>
                <label>{actividad.nombre}</label>
                <div className="radio-buttons">
                  <input
                    type="radio"
                    name={actividad.nombre}
                    value="0"
                    defaultChecked
                    checked={actividad.nivel === 0}
                    onChange={(e) => handleActividadReservadaChange(e, index)}
                    disabled={modoLectura}
                  />
                  Nada
                  <input
                    type="radio"
                    name={actividad.nombre}
                    value="1"
                    checked={actividad.nivel === 1}
                    onChange={(e) => handleActividadReservadaChange(e, index)}
                    disabled={modoLectura}
                  />
                  Bajo
                  <input
                    type="radio"
                    name={actividad.nombre}
                    value="2"
                    checked={actividad.nivel === 2}
                    onChange={(e) => handleActividadReservadaChange(e, index)}
                    disabled={modoLectura}
                  />
                  Medio
                  <input
                    type="radio"
                    name={actividad.nombre}
                    value="3"
                    checked={actividad.nivel === 3}
                    onChange={(e) => handleActividadReservadaChange(e, index)}
                    disabled={modoLectura}
                  />
                  Alto
                </div>
              </div>
            ))}
          </SeleccionConModal>
        </InputOutsideContainer>
        <WholeWidthInputContainer>
          <DoubleSelectionInput
            datosParaSeleccion={datosListaSeleccionDescriptores}
            titulo="DESCRIPTORES"
            mensajeDeError={erroresPrograma.descriptores.descriptores}
            handleListChange={handleDescriptorChange}
          />
        </WholeWidthInputContainer>
      </Formulario>
    </SeccionFormulario>
  )
}
