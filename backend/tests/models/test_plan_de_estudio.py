from django.test import TestCase
from django.utils import timezone

from backend.models import PlanDeEstudio, Carrera
from backend.common.funciones_fecha import obtener_fecha_actual
from backend.tests.utils import set_up_tests


class TestPlanDeEstudio(TestCase):
    # Testeo de las propiedades del modelo de plan de estudio
    def setUp(self) -> None:
        set_up_tests()
        self.carrera = Carrera.objects.all().first()

        self.plan = PlanDeEstudio.objects.create(
            fecha_inicio=obtener_fecha_actual() - timezone.timedelta(days=7),
            version=2,
            nombre="Nombre plan",
            carrera=self.carrera,
        )

    def test_fecha_inicio_posterior_a_fecha_actual(self):
        self.plan.fecha_inicio = obtener_fecha_actual() + timezone.timedelta(days=1)
        self.plan.full_clean()
        self.plan.save()
        self.assertFalse(self.plan.esta_activo)

    def test_fecha_inicio_anterior_a_fecha_actual_y_fecha_fin_indefinido(self):
        self.assertTrue(self.plan.esta_activo)

    def test_fecha_inicio_anterior_a_fecha_actual_y_fecha_fin_definido_posterior_a_fecha_actual(
        self,
    ):
        self.plan.fecha_fin = obtener_fecha_actual() + timezone.timedelta(days=7)
        self.plan.full_clean()
        self.plan.save()
        self.assertTrue(self.plan.esta_activo)

    def test_fecha_inicio_anterior_a_fecha_actual_y_fecha_fin_definido_anterior_a_fecha_actual(
        self,
    ):
        self.plan.fecha_fin = obtener_fecha_actual() - timezone.timedelta(days=1)
        self.plan.full_clean()
        self.plan.save()
        self.assertFalse(self.plan.esta_activo)
