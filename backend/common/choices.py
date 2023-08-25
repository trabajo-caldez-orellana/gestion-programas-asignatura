from django.db.models import TextChoices, IntegerField


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


class NivelDescriptor(IntegerField):
    NADA = 0, "Nada"
    BAJO = 1, "Bajo / Si"
    MEDIO = 2, "Medio"
    ALTO = 3, "Alto"


class TipoCorrelativa(TextChoices):
    REGULAR = "R", "Regular"
    APROBADO = "A", "Aprobado"
