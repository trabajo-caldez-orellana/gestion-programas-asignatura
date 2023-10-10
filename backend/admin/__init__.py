from django.contrib import admin

from .user import UserAdmin
from .actividad_reservada import AdminActividadReservada
from .asignatura import AdminAsignatura
from .auditoria_version_programa import AdminAuditoriaEstadoVersionPrograma
from .bloque_curricular import AdminBloqueCurricular
from .carrera import AdminCarrera
from .configuracion import AdminConfiguracion
from .descriptor import AdminDescriptor
from .estandar import AdminEstandar
from .notificacion import AdminNotificacion
from .plan_de_estudio import AdminPlanDeEstudio
from .semestre import AdminSemestre
from .version_programa_asignatura import AdminVersionProgramaAsignatura

from backend.models import (
    Asignatura,
    AuditoriaEstadoVersionPrograma,
    BloqueCurricular,
    CargaBloque,
    Carrera,
    Configuracion,
    Descriptor,
    Estandar,
    Notificacion,
    PlanDeEstudio,
    Semestre,
    Usuario,
    VersionProgramaAsignatura,
    ActividadReservada,
)

admin.site.register(Usuario, UserAdmin)
admin.site.register(ActividadReservada, AdminActividadReservada)
admin.site.register(Asignatura, AdminAsignatura)
admin.site.register(AuditoriaEstadoVersionPrograma, AdminAuditoriaEstadoVersionPrograma)
admin.site.register(BloqueCurricular, AdminBloqueCurricular)
admin.site.register(Carrera, AdminCarrera)
admin.site.register(Configuracion, AdminConfiguracion)
admin.site.register(Descriptor, AdminDescriptor)
admin.site.register(Estandar, AdminEstandar)
admin.site.register(Notificacion, AdminNotificacion)
admin.site.register(PlanDeEstudio, AdminPlanDeEstudio)
admin.site.register(Semestre, AdminSemestre)
admin.site.register(VersionProgramaAsignatura, AdminVersionProgramaAsignatura)
