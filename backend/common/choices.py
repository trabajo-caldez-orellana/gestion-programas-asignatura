from django.db.models import TextChoices, IntegerChoices


class TipoDescriptor(TextChoices):
    EJE_TRANSVERSAL = ("E", "Eje Transversal")
    DESCRIPTOR = "D", "Descriptor"


class Semestres(TextChoices):
    PRIMER = ("PS", "Primer Semestre")
    SEGUNDO = ("SS", "Segundo Semestre")


class MetodologiaAsignatura(TextChoices):
    PRESENCIAL = ("P", "Presencial")
    VIRTUAL = ("V", "Virtual")
    HIBRIDO = "H", "Hibrido"


class EstadoAsignatura(TextChoices):
    ABIERTO = "A", "Abierto"
    PENDIENTE = "P", "Pendiente"
    APROBADO = "AP", "Aprobado"


class NivelDescriptor(IntegerChoices):
    NADA = 0, "Nada"
    BAJO = 1, "Bajo / Si"
    MEDIO = 2, "Medio"
    ALTO = 3, "Alto"


class TipoCorrelativa(TextChoices):
    REGULAR = "R", "Regular"
    APROBADO = "A", "Aprobado"


# TODO: preguntar que tipo de notificaciones habria que mandar
class TipoNotificacion(TextChoices):
    VERSION_PENDIENTE = "VP", "Version pendiente para correccion"


class Roles(TextChoices):
    DIRECTOR_CARRERA = "DC", "Director de Carrera"
    TITULAR_CATEDRA = (
        "TC",
        "Titular de Catedra",
    )
    SECRETARIO = (
        "SA",
        "Secretario Academico",
    )
    DOCENTE = "D", "Docente"


class Dedicaciones(TextChoices):
    SIMPLE = "N", "No exclusiva"
    EXCLUSIVA = "E", "Exclusiva"


class ParametrosDeConfiguracion(TextChoices):
    INICIO_PERIODO_MODIFICACION = (
        "IPM",
        "Días previos al inicio del Semestre para Modificar el Programa",
    )
    INICIO_PERIODO_VALIDACION = (
        "IPV",
        "Días previos al inicio del Semestre para Validar el Programa",
    )
    INICIO_PERIODO_CORRECCION = (
        "IPC",
        "Días previos al inicio del Semestre para Corregir el Programa",
    )


class EstadosAprobacionPrograma(TextChoices):
    APROBADO = "A", "Aprbado"
    PEDIDO_CAMBIOS = "PC", "Pedir cambios"
    APROBACION_DEPRECADA = "AD", "Aprobacion Deprecada"


class TiposDeEmail(TextChoices):
    RECORDATORIO_PROGRAMA_NUEVO_ASIGNATURA = (
        "recordatorio_asignatura",
        "Recordatorio para crear un programa de asignatura.",
    )
    RECORDATORIO_CORRECION_PROGRAMA = (
        "recordatorio_correccion",
        "Recordatorio para corregir un programa de asignatura",
    )
    PROGRAMA_APROBADO = "programa_aprobado", "El programa fue aprobado"
    CAMBIOS_PEDIDOS = "cambio", "Se pidieron cambios al programa"
    PERIODO_MODIFICACION_ABIERTO = (
        "periodo_modificacion",
        "El periodo para modificar/crear programas de asignatura se ha abierto",
    )
    PROGRAMA_LISTO_PARA_CORRECCION = (
        "pendiente_correccion",
        "El programa esta pendiente de ser corregido",
    )


class RequisitosCorrelativa(TextChoices):
    ASIGNATURA = "asignatura", "Asignatura aprobada o regular"
    CANTIDAD_ASIGNATURAS = "cantidad", "Número de asignaturas aprobadas o regulares"
    MODULO = "modulo", "Módulo aprobado o regular"


class AccionesProgramaDeAsignatura(TextChoices):
    CREAR_NUEVO = "CN", "Crear nuevo programa de asignatura"
    EDITAR = "E", "Editar programa de asignatura"
    PRESENTAR = "P", "Presentar programa de asignatura para aprobación"
    APROBAR = "A", "Aprobar programa de asignatura"
    REUTILIZAR_ULTIMO_PROGRAMA = "RU", "Reutilizar úlitmo programa de asignatura"
    PEDIR_CAMBIOS = "PC", "Pedir cambios en el programa de asignatura"
