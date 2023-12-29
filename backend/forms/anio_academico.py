from typing import Any, Dict
from django import forms

from backend.models import AnioAcademico
from backend.services import ServicioAnioAcademico


class FormAnioAcademico(forms.ModelForm):
    class Meta:
        model = AnioAcademico
        fields = ["fecha_inicio", "fecha_fin"]

    def clean(self) -> Dict[str, Any]:
        datos_validados = super().clean()
        servicio_anio_academico = ServicioAnioAcademico()

        servicio_anio_academico.validar_anio_academico(
            fecha_fin=datos_validados.get("fecha_fin"),
            fecha_inicio=datos_validados.get("fecha_inicio"),
            instance=self.instance,
        )

        return datos_validados
