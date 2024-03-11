from django.utils import timezone


def obtener_fecha_y_hora_actual() -> timezone.datetime:
    return timezone.now().astimezone()


def obtener_fecha_actual() -> timezone.datetime.date:
    return obtener_fecha_y_hora_actual().date()

def crear_fecha_y_hora(
    year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0
):
    return timezone.make_aware(
        timezone.datetime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second
        )
    )

def crear_fecha(
    year: int, month: int, day: int
):
    return timezone.datetime(
            year=year, month=month, day=day
        ).date()

