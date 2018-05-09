# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from catedra import agregar_procesos, stats
from catedra import Proceso
from planificador import Planificador





######################################
######################################
######################################
######################################
######################################

class Proceso:
    """Esta clase representa un proceso con sus caracteristicas básicas para
    simular una planificación de procesos.
    """
    def __init__(self, proc_id=None, estado='listo', rafaga=None,
                funcion=None):
        """Un proceso tiene los siguientes atributos:
        proc_id: id del proceso. Cada proceso tiene un único id y existe un único
        proceso con un cierto id.
        estado: el estado del proceso en un momento dado. Los estados posibles
                son: 'listo', 'ejecutando' y 'terminado'.
                NOTA: el estado es un string.
        prioridad: es la prioridad del proceso. Esto sólo se utilizará en el
                  caso en que el algoritmo utilizado haga uso de las
                  prioridades de los procesos.
        tiempo_inicial: es una marca temporal, se corresponderá con el instante
                        en el que el proceso llega.
        rafaga: es la rafaga de CPU que el proceso necesita para ejecutarse por
                completo. Una vez que se termine este contador, el proceso
                pasará al estado 'terminado'.
        """
        self.proc_id = proc_id
        self.estado = estado
        self.rafaga = rafaga
        self.ya_use = 0
        self.funcion = funcion

    def reset(self):
        self.estado = "listo"

    def mi_estado(self):
        return self.estado

    def cuanto_use(self):
        return self.ya_use

    def enviar_pedido(self, mensaje, proc, clocks):
        """
        mensaje : (arg1, arg2, ..., argN)
        """
        result = proc.recibir_pedido(self, mensaje, clocks)
        return result

    def enviar_resultado(self, proc, mensaje):
        """
        mensaje: es el resultado que se ha obtenido de evaluar la funcion
        """
        return proc.recibir_resultado(mensaje)

    def recibir_pedido(self, proc, mensaje, clocks):
        """
        mensaje : (arg1, arg2, ..., argN)
        """
        self.estado = "listo"

        funcion = self.funcion
        for c in range(min(clocks, self.rafaga - self.ya_use)):
            result = self.ejecutar(funcion, mensaje)
        return self.enviar_resultado(proc, result)


    def recibir_resultado(self, mensaje):
        return mensaje


    def ejecutar(self, funcion, argumentos):
        """Este método ejecuta durante un instante de tiempo el proceso.
        Mientra el proceso está ejecuntándose, su estado será "ejecutando".
        Una vez que haya finalizado su tiempo de ráfaga, el estado pasará a ser
        "terminado".

        IMPORTANTE: Si no termina de ejecutarse, pasa a estar en estado "Listo"
        """
        self.estado = "ejecutando"
        self.ya_use += 1
        if self.rafaga == self.ya_use:
            self.estado = "terminado"
            self.ya_use = 0
            return funcion(*argumentos)
        else:
            self.estado = "listo"
            return None
        ################






######################################
######################################
######################################
######################################
######################################






def suma(a, b):
    return a + b


def prod(a, b):
    return a * b


def div(a, b):
    assert b != 0, "La división por 0 no está definida!"
    return a / b


funciones_ponderadas = {
    'suma': {'funcion': suma, 'rafaga': 5},
    'prod': (prod, 3),
    'div': (div, 3),
}



proceso_padre = Proceso(proc_id=1)
f_suma = funciones_ponderadas['suma']
proceso_suma = Proceso(proc_id=2, **f_suma)
print(proceso_padre.enviar_pedido((1, 3), proceso_suma, 4))
print(proceso_suma.rafaga)
print(proceso_suma.ya_use)
print(proceso_suma.estado)
proceso_suma.reset()













class TestComunicacionProcesos(TestCase):

    def test_suma(self):
        print("Vamos a sumar 5 más 3!")
        # identidad
        proceso_padre = Proceso(proc_id=1)
        proceso_suma = Proceso(proc_id=2, funcion=suma)

        print(proceso_padre.enviar_pedido((1, 3), proceso_suma))
#        for p in mis_procesos:
#            self.assertEqual(estado_real['pids'], promedio)
#
#        self.planificador = Planificador('fcfs')
