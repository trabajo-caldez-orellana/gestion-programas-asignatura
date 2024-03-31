from backend.common.choices import AccionesProgramaDeAsignatura
from backend.models import Rol, VersionProgramaAsignatura, AuditoriaRevisionDocentes

class ServicioAuditoria:
    def auditar_revision(self, rol: Rol, programa: VersionProgramaAsignatura, accion: AccionesProgramaDeAsignatura):
        auditoria = AuditoriaRevisionDocentes(
            rol=rol,
            version_programa=programa,
            accion=accion
        )
        auditoria.full_clean()
        auditoria.save()