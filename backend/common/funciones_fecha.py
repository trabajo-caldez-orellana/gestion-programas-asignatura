from django.utils import timezone


def obtener_fecha_y_hora_actual() -> timezone.datetime:
    return timezone.now().astimezone()


def obtener_fecha_actual() -> timezone.datetime.date:
    return obtener_fecha_y_hora_actual().date()
