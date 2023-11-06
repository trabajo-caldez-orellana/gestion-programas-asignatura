from typing import Any, Dict
from django import forms

from backend.models import Semestre
from backend.services import ServicioSemestre


class FormSemestre(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = ["fecha_inicio", "fecha_fin"]

    def clean(self) -> Dict[str, Any]:
        servicio_semestre = ServicioSemestre()
        datos_validados = super().clean()

        servicio_semestre.validar_semestre(
            fecha_fin=datos_validados.get("fecha_fin"),
            fecha_inicio=datos_validados.get("fecha_inicio"),
            instance=self.instance,
        )

        return datos_validados
