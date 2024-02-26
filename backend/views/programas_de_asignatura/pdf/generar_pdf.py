from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from backend.models import VersionProgramaAsignatura, Correlativa, Estandar, ProgramaTieneDescriptor
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from backend.common.choices import TipoCorrelativa, NivelDescriptor
from backend.models import VersionProgramaAsignatura, Rol
from backend.services import ObtenerDatosPdf
from backend.serializers import serializer_programa_asignatura
from backend.common.mensajes_de_error import (
    MENSAJE_ID_INEXISTENTE,
    MENSAJE_PERMISO_PROGRAMA,
)
from backend.common.choices import TipoDescriptor

class GenerarPDF(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_programa):

        
        datos_programa = ObtenerDatosPdf.obtener_datos_programa(id_programa)

        context =  {
            "programa": datos_programa["programa"],
            "asignatura": datos_programa["asignatura"],
            "docentes": datos_programa["docentes"],
            "carreras": datos_programa["carreras"],
            "correlativas_regular": datos_programa["correlativas_regular"],
            "correlativas_aprobado": datos_programa["correlativas_aprobado"],
            "anio_academico": datos_programa["anio_academico"],
            "resultados_de_aprendizaje": datos_programa["resultados_de_aprendizaje"],
            "ejes_transversales": datos_programa["ejes_transversales"],
            "bloque_curricular": datos_programa["bloque_curricular"],
        }

        template = get_template("programa_de_asignatura.html")

        # Renderiza el template con el contexto
        html_content = template.render(context)

        # Convierte el contenido HTML en un PDF utilizando WeasyPrint
        pdf_file = HTML(string=html_content).write_pdf()

        # Devuelve el PDF como una respuesta HTTP
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="programa.pdf"'
        return response
