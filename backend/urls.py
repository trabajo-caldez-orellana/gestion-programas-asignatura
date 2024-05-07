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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt import views as jwt_views

from backend.views import (
    ListarProgramasVigentesAPI,
    ObtenerFiltros,
    ListarProgramasPendientesAPI,
    InformacionProgramaAPI,
    InformacionModificacionProgramaAPI,
    InformacionNuevoProgramaAPI,
    ModificarProgramaAPI,
    NuevoProgramaAPI,
    InformacionEditarProgramaAPartirDelUltimoAPI,
    ObtenerProgramasHistorial,
    GenerarPDF,
    GoogleLoginApi,
    GoogleAuthApi,
    GenerarMatriz,
    APIListarPlanesDeEstudio,
    AprobarVersionProgramaAPI,
    PedirCambiosVersionProgramaAPI,
    AsignaturasDisponiblesAPartirAsignatura,
    AsignaturasDisponiblesAPartirPrograma,
    LogoutAPI,
)

informes_patterns = [
    path("matriz/<id_carrera>/<id_plan_de_estudio>/", GenerarMatriz.as_view()),
]

programas_patterns = [
    path("pendientes/", ListarProgramasPendientesAPI.as_view()),
    path("vigentes/", ListarProgramasVigentesAPI.as_view()),
    path("pdf/<id_programa>/", GenerarPDF.as_view()),
    path("editar/<id_programa>/", ModificarProgramaAPI.as_view()),
    path("nuevo/<id_asignatura>/", NuevoProgramaAPI.as_view()),
    path("aprobar/<id_programa>/", AprobarVersionProgramaAPI.as_view()),
    path("pedir_cambios/<id_programa>/", PedirCambiosVersionProgramaAPI.as_view()),
    path("<id_programa>/", InformacionProgramaAPI.as_view()),
]

formularios_patterns = [
    path("nuevo/<id_asignatura>/", InformacionNuevoProgramaAPI.as_view()),
    path(
        "editar_ultimo/<id_asignatura>/",
        InformacionEditarProgramaAPartirDelUltimoAPI.as_view(),
    ),
    path(
        "editar/<id_programa>/",
        InformacionModificacionProgramaAPI.as_view(),
    ),
]

opciones_patterns = [
    path(
        "asignaturas-correlativas-programa/<id_programa>/",
        AsignaturasDisponiblesAPartirPrograma.as_view(),
    ),
    path(
        "asignaturas-correlativas/<id_asignatura>/",
        AsignaturasDisponiblesAPartirAsignatura.as_view(),
    ),
]

filtros_patterns = [
    path("", ObtenerFiltros.as_view()),
]

historial_patterns = [
    path("", ObtenerProgramasHistorial.as_view()),
]

planes_estudio_patterns = [
    path("", APIListarPlanesDeEstudio.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/logout/", LogoutAPI.as_view()),
    path("auth/login/google/", GoogleLoginApi.as_view(), name="login-with-google"),
    path("auth/me/", GoogleAuthApi.as_view()),
    path("api/programas/", include(programas_patterns)),
    path("api/filtros/", include(filtros_patterns)),
    path("api/historial/", include(historial_patterns)),
    path("api/informacion-formularios/", include(formularios_patterns)),
    path("api/informes/", include(informes_patterns)),
    path("api/planes-de-esutdio/", include(planes_estudio_patterns)),
    path("api/opciones/", include(opciones_patterns)),
    re_path(
        "<path:route>", TemplateView.as_view(template_name="index.html"), name="index"
    ),
    re_path("", TemplateView.as_view(template_name="index.html"), name="index"),
]
