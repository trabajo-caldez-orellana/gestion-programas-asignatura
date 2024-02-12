"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from backend.views import (
    ListarProgramasVigentesAPI,
    ObtenerFiltrosHistorial,
    ListarProgramasPendientesAPI,
    InformacionProgramaAPI,
    InformacionModificacionProgramaAPI,
    InformacionNuevoProgramaAPI,
    ModificarProgramaAPI
)

programas_patterns = [
    path("pendientes/", ListarProgramasPendientesAPI.as_view()),
    path("vigentes/", ListarProgramasVigentesAPI.as_view()),
    path("<id_programa>/", InformacionProgramaAPI.as_view()),
    path(
        "informacion_modificion/<id_programa>/",
        InformacionModificacionProgramaAPI.as_view(),
    ),
    path("informacion_nuevo/<id_asignatura>/", InformacionNuevoProgramaAPI.as_view()),
    # TODO. Crear una API nueva para editar el ultimo!!
    path("informacion_editar_ultimo/<id_asignatura>/", InformacionNuevoProgramaAPI.as_view()),
    path("modificar-programa/<id-programa>/", ModificarProgramaAPI.as_view())
]

historial_patterns = [
    path("", ObtenerFiltrosHistorial.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.social.urls")),
    path("api/programas/", include(programas_patterns)),
    path("api/historial/", include(historial_patterns)),
]
