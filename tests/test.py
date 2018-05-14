# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from proceso import Proceso, ProcesoNoListo


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

    def test_no_termino_prod(self):
        proceso_padre = Proceso(proc_id=1)
        f_prod = funciones_ponderadas['prod']
        proceso_prod = Proceso(proc_id=2, **f_prod)
        result = proceso_padre.enviar_pedido((4, 2), proceso_prod, 5)

        self.assertEqual(result, None)
        self.assertEqual(proceso_prod.ya_use + 3, proceso_prod.rafaga)
        self.assertEqual(proceso_prod.estado, 'listo')

        result = proceso_padre.enviar_pedido((4, 2), proceso_prod, 3)
        self.assertEqual(result, 8)
        self.assertEqual(proceso_prod.ya_use, proceso_prod.rafaga)
        self.assertEqual(proceso_prod.estado, 'terminado')

    def test_reset_div(self):
        proceso_padre = Proceso(proc_id=1)
        f_div = funciones_ponderadas['div']
        proceso_div = Proceso(proc_id=2, **f_div)
        result = proceso_padre.enviar_pedido((3, 1), proceso_div, 8)

        self.assertEqual(result, 3)
        self.assertEqual(proceso_div.ya_use, proceso_div.rafaga)
        self.assertEqual(proceso_div.estado, 'terminado')

        proceso_div.reset()
        self.assertEqual(proceso_div.ya_use, 0)
        self.assertEqual(proceso_div.estado, 'listo')

    def test_ej_combinado_no_listo(self):
        """
        20/4 + (4 * 3) + 1
        """
        proceso_padre = Proceso(proc_id=1)
        f_suma = funciones_ponderadas['suma']
        proceso_suma = Proceso(proc_id=2, **f_suma)

        f_prod = funciones_ponderadas['prod']
        proceso_prod = Proceso(proc_id=3, **f_prod)

        f_div = funciones_ponderadas['div']
        proceso_div = Proceso(proc_id=4, **f_div)

        mi_prod = proceso_padre.enviar_pedido((4, 3), proceso_prod, 8)
        suma_parc = proceso_padre.enviar_pedido((mi_prod, 1), proceso_suma, 5)

        mi_div = proceso_padre.enviar_pedido((20, 4), proceso_div, 8)

        try:
            ret = proceso_padre.enviar_pedido((mi_div, suma_parc), proceso_suma, 5)
        except ProcesoNoListo:
            self.assertTrue(True)



    def test_ej_combinado(self):
        """
        20/4 + (4 * 3) + 1
        """
        proceso_padre = Proceso(proc_id=1)
        f_suma = funciones_ponderadas['suma']
        proceso_suma = Proceso(proc_id=2, **f_suma)

        f_prod = funciones_ponderadas['prod']
        proceso_prod = Proceso(proc_id=3, **f_prod)

        f_div = funciones_ponderadas['div']
        proceso_div = Proceso(proc_id=4, **f_div)

        mi_prod = proceso_padre.enviar_pedido((4, 3), proceso_prod, 8)
        suma_parc = proceso_padre.enviar_pedido((mi_prod, 1), proceso_suma, 5)

        mi_div = proceso_padre.enviar_pedido((20, 4), proceso_div, 8)

        proceso_suma.reset()
        ret = proceso_padre.enviar_pedido((mi_div, suma_parc), proceso_suma, 5)

        self.assertEqual(ret, 18)
