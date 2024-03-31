from backend.common.choices import AccionesProgramaDeAsignatura
from backend.models import Usuario, VersionProgramaAsignatura, AuditoriaRevisionDocentes

class ServicioAuditoria:
    def auditar_revision(self, usuario: Usuario, programa: VersionProgramaAsignatura, accion: AccionesProgramaDeAsignatura):
        auditoria = AuditoriaRevisionDocentes(
            usuario=usuario,
            version_programa=programa,
            accion=accion
        )
        auditoria.full_clean()
        auditoria.save()