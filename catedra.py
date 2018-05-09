import texttable as tt
from numpy import mean
import csv




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
        # Para enviar un pedido, lo que hacemos el llamar al método
        # recibir_pedido del OTRO proceso, con los parámetros adecuados.
        result = proc.recibir_pedido(self, mensaje, clocks)
        return result

    def enviar_resultado(self, proc, mensaje):
        """
        Éste método envía el resultado (el "mensaje") al proceso correspondiente.
        
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



class ProcesoSinRafaga(Exception):
    """Esta clase representa la excepción que ocurre cuando se quiere ejecutar
    un proceso que no tiene más ráfaga.
    """
    pass


class CPU:
    """Esta clase representa el cpu de una máquina. Ella ejecutará procesos
    conforme se los brinden.
    """
    def __init__(self):
        """El cpu, en esta caso (muy) simplificado para enfocar la atención a
        la ejecución de los procesos, tendrá como atributos:
        proc: proceso que está ejecutando en un momento dado.
        run_time: tiempo total de ejecución (para simplificación, sólo se
                  contará el tiempo en que haya un proceso en la cpu)
        """
        self.run_time = 0

    def ejecutar(self, proceso):
        """Este método ejecuta un proceso en la CPU.
        Se encargará de cambiar el estado a 'terminado' en caso de ser
        necesario, pero NO lo cambiará a 'listo'.
        Asignar el tiempo una vez que se termine de ejecutar el proceso será
        responsabilidad del planificador.
        """
        if proceso.tiempo_inicial is None:
            proceso.tiempo_inicial = self.run_time
        if proceso.estado == "terminado":
            raise ProcesoSinRafaga("El proceso ha terminado de ejecutarse!")

        proceso.ejecutar()
        self.run_time += 1

    def gettime(self):
        """Este método retorna el tiempo total que ha ejecutado la CPU en el
        momento en que se lo invoca.
        """
        return self.run_time

###############################################################################


def table(procesos, headers):
    """Toma una lista de procesos (instancias de la clase Proceso), confecciona
    una tabla con los datos de cada uno.
    Esta función se usará para mostrar la instancia del problema inicial, una
    vez que se cargan desde el archivo.
    Notar que para este caso, le pasamos como argumento los nombres de las
    columnas.
    """
    # Aquí creamos cada columna
    pids = [proc.proc_id for proc in procesos]
    rafagas = [proc.rafaga for proc in procesos]
    tiempos_arribo = [proc.tiempo_arribo for proc in procesos]

    table = tt.Texttable()
    table.header(headers)

    if len(headers) == 4:
        prioridades = [proc.prioridad for proc in procesos]
        filas = zip(pids, rafagas, tiempos_arribo, prioridades)
    else:
        filas = zip(pids, rafagas, tiempos_arribo)
    for fila in filas:
        table.add_row(fila)

    tabla = table.draw()
    return tabla


def stats(procesos):
    """Toma una lista de procesos (instancias de la clase Proceso), confecciona
    una tabla con los datos de cada uno y calcula el promedio de espera de
    todos los procesos
    """
    # Estas serán las etiquetas de las columnas
    headears = ["PID", "Ráfaga", "T Arribo",
                "T Inicial", "T Final", "Tiempo Total"]

    # Aquí creamos cada columna
    pids = [proc.proc_id for proc in procesos]
    rafagas = [proc.rafaga for proc in procesos]
    tiempos_arribo = [proc.tiempo_arribo for proc in procesos]
    tiempos_iniciales = [proc.tiempo_inicial for proc in procesos]
    tiempos_finales = [proc.end_time for proc in procesos]

    tiempos_totales = [tf - ta for ta, tf in zip(tiempos_arribo,
                                                 tiempos_finales)]
    tiempos_espera = [tt - r for tt, r in zip(tiempos_totales,
                                              rafagas)]
    promedio_espera = mean(tiempos_espera)
    table = tt.Texttable()
    table.header(headears)

    for fila in zip(pids, rafagas, tiempos_arribo, tiempos_iniciales,
                    tiempos_finales, tiempos_totales):
        table.add_row(fila)

    tabla = table.draw()

    datos_testing = dict()
    datos_testing['pids'] = pids
    datos_testing['rafagas'] = rafagas
    datos_testing['tiempos_finales'] = tiempos_finales
    datos_testing['tiempos_totales'] = tiempos_totales
    datos_testing['tiempos_espera'] = tiempos_espera
    datos_testing['promedio'] = promedio_espera
    return tabla, promedio_espera, datos_testing


def agregar_procesos(planificador, filename):
    """Esta función leerá el archivo que contiene una instancia de procesos.
    A partir de él, creará los procesos correspondientes y utilizará métodos
    del planificador para que éste último se haga de ellos.
    Además, la función imprimirá por consola una tabla con la instancia que
    ha cargado del archivo.
    """
    procesos = []
    with open(filename, 'r') as f:
        i = 0
        reader = csv.reader(f)
        for proc_info in reader:
            if i == 0:
                headers = proc_info
                i += 1
                continue
            proc_id = proc_info[0]
            rafaga = int(proc_info[1])
            tiempo_arribo = int(proc_info[2])
            # Si el algoritmo que vamos a usar no utiliza la prioridad,
            # no se tendrá en cuenta la misma
            prioridad = None
            if len(proc_info) == 4:
                prioridad = int(proc_info[3])
            proc = Proceso(proc_id=proc_id, rafaga=rafaga, tiempo_arribo=tiempo_arribo,
                           prioridad=prioridad)
            planificador.entra_proceso(proc)
            procesos.append(proc)
    estado_inicial = table(procesos, headers)
    print(estado_inicial)
