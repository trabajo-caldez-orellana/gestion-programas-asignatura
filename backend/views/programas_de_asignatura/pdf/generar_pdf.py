from weasyprint import HTML

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
from django.template.loader import get_template

from backend.services import ObtenerDatosPdf


class GenerarPDF(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, id_programa):
        servicio_obtener_datos =ObtenerDatosPdf()
        datos_programa = servicio_obtener_datos.obtener_datos_programa(id_programa)

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
