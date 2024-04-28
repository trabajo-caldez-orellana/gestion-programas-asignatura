# MENSAJES COMUNES
MENSAJE_FECHAS_INCORRECTAS = "Fecha fin mayor o igual a fecha inicio."
MENSAJE_NIVEL_INVALIDO = "El nivel seleccionado no es un valor valido."
MENSAJE_CAMPO_ENTERO = "Este campo debe ser un numero entero mayor a cero."
MENSAJE_CAMPO_NO_NULO = "Este campo no puede ser nulo."
MENSAJE_CAMPO_EN_BLANCO = "Este campo no puede estar en blanco."
MENSAJE_ERROR_INESPERADO = (
    "Un error inesperado ha ocurrido. Intente nuevamente más tarde."
)

# Mensajes relacionados a usuarios
MENSAJE_SUPERUSUARIO_ACTIVO = "Superusuario deberia estar activo."
MENSAJE_SUPERUSUARIO = "Superusuario deberia estar marcado como superusuario."
MENSAJE_SUPERUSUARIO_STAFF = "Superusuario deberia ser staff."
MENSAJE_EMAIL_NO_PROPORCIONADO = "Email no proporcionado."


# Mensajes relacionados a roles
MENSAJE_DIRECTOR_SELECCIONA_CARRERA = (
    "El Director de Carrera debe seleccionar una Carrera."
)
MENSAJE_DIRECTOR_SELECCIONA_ASIGNATURA = (
    "El Director de Carrera no debe seleccionar una Asignatura."
)
MENSAJE_DOCENTE_SELECCIONA_CARRERA = "No debe seleccionar una Carrera."
MENSAJE_DOCENTE_SELECCIONA_ASIGNATURA = "Debe seleccionar Asignatura."
MENSAJE_SECRETARIO_SELECCIONA_ASIGNATURA_O_CARRERA = (
    "El Secretario Academico no debe seleccionar Carrera o Asignatura."
)


# Mensaje relacionados a la asignatura
CODIGO_ASIGNATURA_INCORRECTO = "El codigo de la asignatura debe comenzar con '15_', y continuar con tres caracteres en mayuscula."
MENSAJE_HORARIO_BLOQUEADO_PARA_METODOLOGIA = "No debe asignar un valor a este horario."
MENSAJE_HORARIO_REQUERIDO_PARA_METODOLOGIA = (
    "Asignar un valor a este horario es requerido."
)


# Mensajes relacionados al Programa de asignatura
MENSAJE_FORMATO_DESCRIPTORES_INVALIDO = (
    "El formato provisto para los descriptores es incorrecto."
)
MENSAJE_FORMATO_EJES_TRANSVERSALES_INVALIDO = (
    "El formato provisto para los ejes transversales es incorrecto."
)
MENSAJE_FORMATO_ACTIVIDADES_RESERVADAS_INVALIDO = (
    "El formato provisto para las actividades reservadas es incorrecto."
)
MENSAJE_EJE_TRANSVERSAL_INVALIDO = "Un eje transversal seleccionado no es valido."
MENSAJE_ACTIVIDAD_RESERVADA = "Una actividad reservada seleccionada no pertenece a ninguna de las carreras a las que pertenece la asignatura."
MENSAJE_DESCRIPTOR = "Un descriptor seleccionado no pertenece a ninguna de las carreras a las que pertenece la asignatura."
MENSAJE_EJE_TRANSVERAL = "Un eje transversal seleccionado no pertenece a ninguna de las carreras a las que pertenece la asignatura."
MENSAJE_NIVEL_INCORRECTO = "Descriptor solo puede tener nivel 0 o 1."
MENSAJE_RESULTADOS_CON_FORMATO_INCORRECTO = (
    "Los resultados de aprendizaje deben ser una lista."
)
MENSAJE_NO_HAY_PROGRAMAS_EXISTENTES = (
    "La asignatura seleccionada todavia no tiene programas de asignatura."
)
MENSAJE_CANTIDAD_DE_RESULTADOS = (
    "Un programa debe tener entre 5 a 8 resultados de aprendizaje."
)
MENSAJE_PROGRAMAS_CERRADOS = (
    "No es posible crear o modificar versiones de Programas de Asignatura actualmente."
)
MENSAJE_VERSION_ANTERIOR_NO_APROBADA = "La version anterior a la que se quiere acceder no fue aprobadda todavia, por lo que no se puede realizar una copia."
MENSAJE_PROGRAMA_DEBE_TENER_DESCRIPTOR = (
    "El programa debe tener al menos un descriptor."
)
MENSAJE_PROGRAMA_DEBE_TENER_EJE_TRANSVERSAL = (
    "El programa debe tener al menos un eje transversal."
)
MENSAJE_PROGRAMA_DEBE_TENER_ACTIVIDAD_RESERVADA = (
    "El programa debe tener al menos una actividad reservada."
)
MENSAJE_DESCRIPTOR_INVALIDO = "Un descriptor seleccionado no es valido."
MENSAJE_ACTIVIDAD_RESERVADA_INVALIDA = (
    "Una actividad reservada seleccionada no es valido."
)
MENSAJE_SEMESTRE_DEBE_PERTENECER_A_ANIO_LECTIVO = (
    "Las fechas del semestre deben estar dentro del anio lectivo seleccionado."
)
MENSAJE_ID_INEXISTENTE = "El ID provisto no es valido."
MENSAJE_PROGRAMA_APROBADO = "No es posible modificar un programa que ya fue aprobado."
MENSAJE_PROGRAMA_YA_EXISTENTE = (
    "Ya fue creado un programa para la asignatura para el semestre siguiente."
)
MENSAJE_NO_TIENE_PERMISO_PARA_CORREGIR = (
    "No puede corregir un programa de asignatura porque no tiene los permisos."
)
MENSAJE_PROGRAMA_NO_SE_ENCUENTRA_DISPONIBLE_PARA_CORREGIR = (
    "El programa no esta disponible para ser corregido."
)
MENSAJE_REQUISITO_CORRELATIVA_INVALIDO = (
    "El requisito para la correlativa elegido es inválido."
)
MENSAJE_TIPO_CORRELATIVA_INVALIDO = "El tipo de correlativa elegido es inválido."
MENSAJE_ASIGNATURA_NECESARIA = "Si la correlativa tiene como requerimiento una asignatura, se debe seleccionar una asignatura válida."
MENSAJE_CANTIDAD_ASIGNATURAS_NECESARIA = "Si la correlativa tiene como requerimiento una cantidad de asignaturas aprobadas o regulares, se debe indicar un número de asignaturas."
MENSAJE_MODULO_NECESARIO = "Si la correlativa tiene como requerimiento un módulo aprobado o regular, se debe indicar el módulo."
MENSAJE_CORRELATIVA_INVALIDA = "El objeto de correlativa recibido es invalido."

# Mensajes relacionados a semestres y anios lectivos
MENSAJE_NO_PUEDEN_HABER_VARIOS_SEMESTRES_CON_LA_MISMA_FECHA = "No se puede definir un semestre que este activo al mismo momento que otro. Verifique las fechas."
MENSAJE_NO_PUEDEN_HABER_VARIOS_ANIOS_ACADEMICOS_CON_LA_MISMA_FECHA = "No se puede definir un año académico que este activo al mismo momento que otro. Verifique las fechas."
MENSAJE_NO_HAY_SEMESTRE_ACTIVO = "No hay un semestre activo."
MENSAJE_NO_HAY_SEMESTRES_ANTERIORES = "No hay semestres anteriores."
MENSAJE_NO_HAY_SEMESTRES_FUTUROS = "No hay semestres futuros."
MENSAJE_NO_HAY_ANIO_ACTIVO = "No hay un año académico activo."
MENSAJE_NO_HAY_ANIOS_ANTERIORES = "No hay años académicos anteriores."
MENSAJE_NO_HAY_ANIOS_FUTUROS = "No hay años académicos futuros."
MENSAJE_TIPO_SEMESTRE_REPETIDO = (
    "No puede haber dos semestres del mismo tipo para un año académico."
)
MENSAJE_SEGUNDO_SEMESTRE_DESPUES_DEL_PRIMERO = (
    "Un semestre del primer semestre debe tener fecha antes de uno del segundo semeste."
)
MENSAJE_FALLO_REUTILIZACION = (
    "La reutilización del programa fallo. El programa anterior tiene fallas."
)

# Mensajes relacionados a parametros de configuracion
MENSAJE_NO_FUE_DEFINIDO_PERIODO_MODIFICACION = "No se completaron las configuraciones del programa. Debe definir los días para período de modificación."
MENSAJE_NO_FUE_DEFINIDO_PERIODO_VALIDACION = "No se completaron las configuraciones del programa. Debe definir los días para período de validación."
MENSAJE_NO_FUE_DEFINIDO_PERIODO_CORRECCION = "No se completaron las configuraciones del programa. Debe definir los días para período de corrección."
MENSAJE_VERSION_CERRADA_PARA_MODIFICACION = (
    "No se puede modificar un programa pendiente de aprobación o ya aprobado."
)


# MENSAJES DE PERMISOS
MENSAJE_PERMISO_PROGRAMAS_PENDIENTES = (
    "No tiene permiso para accceder a programas pendientes."
)
MENSAJE_PERMISO_PROGRAMA = "No tiene permiso para acceder a este Programa."
MENSAJE_NO_ESTAN_TODOS_LOS_PROGRAMAS = (
    "Faltan programas por aprobar para este año lectivo."
)

# MENSAJES DE APIs
MENSAJE_CARRERA_PLAN = "El programa provisto no pertenece a la carrera provista."
