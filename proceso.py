class ProcesoNoListo(Exception):
    """Esta clase representa la excepción que ocurre cuando se quiere ejecutar
    un proceso que no está listo
    """
    pass


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
        """
        Acá restauramos los valores del Proceso para que pueda volver a ejecutar
        """
        ####################
        # Aquí va su código
        ####################
        pass

    def mi_estado(self):
        """
        Este método simplemente nos devuelve el estado del proceso.
        Se usa como una interfaz del atributo
        """
        return self.estado

    def cuanto_use(self):
        """
        Este método nos dice cuántos clocks se va ejecutando hasta ahora.
        Notar que también es una interfaz del atributo 'ya_use'
        """
        return self.ya_use

    def enviar_pedido(self, mensaje, proc, clocks):
        """
        Este método envía un pedido a cierto proceso. Es decir, le solicita
        al proceso que ejecute la función que lo caracteriza, con los argumentos
        que están en "mensaje" y por una cierta cantidad de clocks
        Devuelve el resultado del pedido.

        Los parámetros de este método son:

        :param mensaje : (arg1, arg2, ..., argN)
        :param proc: Proceso() [es el proceso al que le vamos a pedir la
                    ejecución]
        :param clocks: Int [es la cantidad de clocks que se va a ejecutar la
                            función que caracteriza al proceso]
        """
        ####################
        # Aquí va su código
        ####################

        pass

    def enviar_resultado(self, proc, mensaje):
        """
        Éste método envía el resultado (el "mensaje") al proceso
        correspondiente.

        Los parámetros del método son:

        :param proc: el proceso que al que se le debe enviar el resultado
        :param mensaje: es el resultado que se ha obtenido de evaluar la
                        funcion
        """
        ####################
        # Aquí va su código
        ####################

        pass

    def recibir_pedido(self, proc, argumentos, clocks):
        """
        En este método se recibe el pedido de ejecución de parte del proceso
        que ha realizado la solicitud y se ejecuta la cantidad de clocks que se
        correspondan la función que caracteriza al proceso, con los argumentos
        dados
        Los parámetros del método son:

        :param proc: el proceso que que ha hecho el pedido
        :param argumentos: (arg1, arg2, ..., argN)
        :param clocks: cantidad de clocks que se vaya a ejecutar el proceso
        """
        # Si el proceso no está listo, no puede llevar a cabo el pedido
        if self.estado != "listo":
            raise ProcesoNoListo

        ####################
        # Aquí va su código
        ####################

        pass


    def recibir_resultado(self, mensaje):
        """
        Este método es en el cual el proceso recibe el resultado obtenido
        del pedido que habia realizado

        Su parámetro es:
        :param mensaje: resultado del pedido
        """
        ####################
        # Aquí va su código
        ####################

        pass


    def ejecutar(self, funcion, argumentos):
        """Este método ejecuta durante un instante de tiempo el proceso.
        Una vez que haya finalizado su tiempo de ráfaga, el estado pasará a ser
        "terminado".

        IMPORTANTE: Si no termina de ejecutarse, pasa a estar en estado "Listo"
        """
        ####################
        # Aquí va su código
        ####################

        if self.rafaga == self.ya_use:
            # Si se termino de ejecutar, se evalúa la funcion con los
            # argumentos dados.
            # En este caso, antes de volver a pedir su ejecución, habría que
            # ejecutar el método del proceso 'reset'.

            # Falta hacer algo más con el proceso, antes de la próxima línea?
            return funcion(*argumentos)
        else:
            # Si todavía no se terminó de ejecutar,
            # devuelve None (es un valor nulo)

            # Falta hacer algo más con el proceso, antes de la próxima línea?
            return None
