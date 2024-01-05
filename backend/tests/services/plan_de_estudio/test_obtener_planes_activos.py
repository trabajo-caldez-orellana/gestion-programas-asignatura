from django.test import TestCase


class TestObtenerPlanesActivos(TestCase):
    def test_caso_general(self):
        """
        Testear que se devuelven los activos de:
          - Un plan muy viejo (del 2000) que ya tenga fecha fin anterior al dia actual (No Activo)
          - Un plan viejo (del 2010) que ya tenga fecha fin, pero posterior al dia actual (Activo)
          - Un plan viejo (del 2015) que no tenga fecha fin (Activo)
          - Un plan nuevo (del 2020) que no tenga fecha fin (Activo)
        """
        pass
