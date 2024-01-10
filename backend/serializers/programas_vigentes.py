from rest_framework import serializers

class ProgramasVigentesSerializer(serializers.Serializer):
    def to_representation(self, instance):
        result = []
        for programa in instance:
            asignatura_data = {
                "id": programa.id,
                "asignatura": {
                    "id": programa.asignatura.id,
                    "nombre": programa.asignatura.denominacion
                },
                "estado": programa.estado,
                "id_programa": programa.id,
                "acciones_posibles": {
                    "ver_programa": True,
                },
                "accion_requerida": False
            }
            result.append(asignatura_data)
        return result