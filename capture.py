from lib.formulario import Formulario
from  lib.conexion import Conexion
#from lib.hilo import Hilo
import hashlib as h
from  threading import Thread
import threading
import json


class Capture(Thread):
    max_threads = 20
    semaphore = threading.Semaphore(max_threads)
    
    def __init__(self, task_id):        
        Thread.__init__(self)
        self.task_id = task_id
        self.conn = Conexion()

    def run(self):
        print('Proceso {0}'.format(self.task_id))
        with Capture.semaphore:
            print(f'Actualmente, hay {Capture.max_threads - Capture.semaphore._value} hilos en ejecución.')
            for i in range(100000):
                formulario = Formulario()
                self.conn.send(formulario.formulario_to_json())
        print('Terminado proceso {} '.format(self.task_id))
        self.conn.close()




def launch_tasks(n):
    threads = []
    for i in range(n):
        thread = Capture(i)
        threads.append(thread)
        thread.start()


    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

launch_tasks(1)  # Ejecuta 100 tareas, de 20 en 20.

print('Terminado') 