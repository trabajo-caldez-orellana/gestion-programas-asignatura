from django.db.models import QuerySet

from backend.models import Usuario, Rol, VersionProgramaAsignatura, Asignatura
from backend.common.choices import EstadoAsignatura, Roles


class ServicioRoles:
    def obtener_roles_usuario(self, usuario: Usuario) -> QuerySet[Rol]:
        roles = Rol.objects.filter(usuario=usuario)
        return roles

    def usuario_tiene_permiso_para_crear_programa(
        self, usuario: Usuario, asignatura: Asignatura
    ) -> bool:
        roles = self.obtener_roles_usuario(usuario)

        for rol in roles:
            if (rol.rol == Roles.DOCENTE or rol.rol == Roles.TITULAR_CATEDRA) and rol.asignatura == asignatura:
                return True
        
        return False

    def usuario_tiene_permiso_para_acceder_a_programa(
        self, usuario: Usuario, programa: VersionProgramaAsignatura
    ) -> bool:
        if programa.estado == EstadoAsignatura.APROBADO:
            return True

        roles = self.obtener_roles_usuario(usuario)
        for rol in roles:
            if rol.rol == Roles.SECRETARIO:
                return True

            if rol.rol == Roles.DIRECTOR_CARRERA:
                # Verifica que la carrera tenga esa asignatura!
                planes_relacionados = programa.asignatura.planes_de_estudio.all()
                planes_count = planes_relacionados.filter(carrera=rol.carrera).count()

                if planes_count > 0:
                    return True

            else:
                if rol.asignatura == programa.asignatura:
                    return True

        return False
