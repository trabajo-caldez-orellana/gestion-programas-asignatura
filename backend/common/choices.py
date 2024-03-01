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
