from django.contrib import admin


from .models import (
    Asignatura,
    AuditoriaEstadoVersionPrograma,
    BloqueCurricular,
    CargaBloque,
    Carrera,
    Configuracion,
    Correlativa,
    Descriptor,
    Estandar,
    Notificacion,
    PlanDeEstudio,
    ProgramaTieneDescriptor,
    Rol,
    Semestre,
    Usuario,
    VersionProgramaAsignatura,
)


@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


admin.site.register(Asignatura)
admin.site.register(AuditoriaEstadoVersionPrograma)
admin.site.register(BloqueCurricular)

# TODO. Esto no agregarlo como una sola cosa, sino como una propuedad de Programa de Asignatura
admin.site.register(CargaBloque)

admin.site.register(Carrera)
admin.site.register(Configuracion)

# TODO. Esto no agregarlo como una sola cosa, sino como una propuedad de Programa de Asignatura
admin.site.register(Correlativa)

# TODO. Esto no agregarlo como una sola cosa, sino como una propiedad de el Estandar
admin.site.register(Descriptor)
admin.site.register(Estandar)
admin.site.register(Notificacion)
admin.site.register(PlanDeEstudio)

# TODO. Esto no agregarlo como una sola cosa, sino como una propuedad de Programa de Asignatura
admin.site.register(ProgramaTieneDescriptor)
admin.site.register(Rol)
admin.site.register(Semestre)
admin.site.register(VersionProgramaAsignatura)
