# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from catedra import Proceso


def suma(a, b):
    return a + b


def prod(a, b):
    return a * b


def div(a, b):
    assert b != 0, "La división por 0 no está definida!"
    return a / b


funciones_ponderadas = {
    'suma': {'funcion': suma, 'rafaga': 5},
    'prod': {'funcion': prod, 'rafaga': 8},
    'div': {'funcion': div, 'rafaga': 8},
}



class TestComunicacionProcesos(TestCase):

    def test_termino_suma(self):
        proceso_padre = Proceso(proc_id=1)
        f_suma = funciones_ponderadas['suma']
        proceso_suma = Proceso(proc_id=2, **f_suma)
        result = proceso_padre.enviar_pedido((1, 3), proceso_suma, 5)

        self.assertEqual(result, 4)
        self.assertEqual(proceso_suma.ya_use, proceso_suma.rafaga)
        self.assertEqual(proceso_suma.estado, 'terminado')
