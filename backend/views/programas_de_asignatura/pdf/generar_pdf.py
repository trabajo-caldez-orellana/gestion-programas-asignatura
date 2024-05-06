from weasyprint import HTML, CSS

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
from django.template.loader import get_template

from backend.services import ObtenerDatosPdf


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == "body":
            return box

        return get_page_body(box.all_children())


class GenerarPDF(APIView):
    permission_classes = [
        # IsAuthenticated,
    ]

    def get(self, request, id_programa):
        servicio_obtener_datos = ObtenerDatosPdf()
        datos_programa = servicio_obtener_datos.obtener_datos_programa(id_programa)

        context = {
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

        # Main template
        main_html = get_template("programa_de_asignatura.html")
        main_doc = main_html.render(context)
        main_doc = HTML(string=main_doc).render()

        # Template of header
        header_html = get_template("documento_header.html")
        header = header_html.render()
        header = HTML(string=header)
        header = header.render(
            stylesheets=[
                CSS(
                    string="@page {size:A4; margin:0 1cm;} body {position: fixed; top: 0cm;}"
                )
            ]
        )

        header_page = header.pages[0]
        header_body = get_page_body(header_page._page_box.all_children())
        header_body = header_body.copy_with_children(header_body.all_children())

        # Template of footer
        footer_html = get_template("documento_footer.html")
        footer = footer_html.render()
        footer = HTML(string=footer)
        footer = footer.render(
            stylesheets=[
                CSS(
                    string="@page {size:A4; margin:0 1cm;} body {position: fixed; bottom: 0;}"
                )
            ]
        )

        footer_page = footer.pages[0]
        footer_body = get_page_body(footer_page._page_box.all_children())
        footer_body = footer_body.copy_with_children(footer_body.all_children())

        # Insert header and footer in main doc
        for _, page in enumerate(main_doc.pages):

            page_body = get_page_body(page._page_box.all_children())

            page_body.children += header_body.all_children()
            page_body.children += footer_body.all_children()

        pdf = main_doc.write_pdf()
        # Devuelve el PDF como una respuesta HTTP
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="programa.pdf"'
        return response
