from backend.models import Usuario, Rol


class ServicioRoles:
    def obtener_roles_usuario(self, usuario: Usuario):
        roles = Rol.objects.filter(usuario=usuario)
        print(roles)

        return roles
