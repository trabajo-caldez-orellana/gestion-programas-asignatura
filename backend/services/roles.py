from django.db.models import QuerySet

from backend.models import Usuario, Rol


class ServicioRoles:
    def obtener_roles_usuario(self, usuario: Usuario) -> QuerySet[Rol]:
        roles = Rol.objects.filter(usuario=usuario)

        return roles
