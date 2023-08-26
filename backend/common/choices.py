from django.db.models import TextChoices, IntegerChoices


class TipoDescriptor(TextChoices):
    EJE_TRANSVERSAL = ("E", "Eje Transversal")
    ACT_RESERVADA = ("A", "Actividad Reservada")
    DESCRIPTOR = "D", "Descriptor"


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
