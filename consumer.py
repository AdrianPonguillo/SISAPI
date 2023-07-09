#from collections.abc import Callable, Iterable, Mapping
from  threading import Thread
import threading
import json
import os
#import pickle
#from typing import Any
from lib.conexion import Conexion
import signal

class Repositorio(Thread):
    def __init__(self, user_id, contenido):
        Thread.__init__(self)
        self.name_file = user_id
        self.contenido = contenido
    
    def run(self):
        try:
            # Intentamos guardar en la carpeta database
            with open('./files/' + self.name_file + '.json', 'x') as f:
                json.dump(self.contenido, f, ensure_ascii=False)
        except FileExistsError:
            # Añadir un sufijo al nombre del archivo hasta que encontremos un nombre que no esté en uso
            suffix = 1
            while True:
                try:                    
                    with open('./files/duplicados/' + self.name_file + '_' + str(suffix) + '.json', 'x') as f:
                        json.dump(self.contenido, f)
                    break  # Salir del ciclo una vez que el archivo se ha escrito con éxito
                except FileExistsError:
                    suffix += 1  # Incrementar el sufijo y probar con el siguiente número



class ConsumerThread(Thread):
    file_lock = threading.Lock()

    def __init__(self):
        self.conn = Conexion()
        threading.Thread.__init__(self)
        self.index_table = {}
        self.file_pointer = 0
    
    def close_connection(self):
        self.conn.close()

    def callback(self, ch, method, properties, body):
        
        message_dict = json.loads(body)
        # Extrae el UUID y user_id
        uuid_key, user_info = next(iter(message_dict.items()))
        user_id = user_info["informacion_personal"]["user_id"]

        repositorio = Repositorio(user_id= user_id, contenido = message_dict)
        repositorio.start()
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.conn.consuming(self.callback)
        self.conn.close()



def signal_handler(sig, frame):
    print('Presionaste Ctrl+C!')
    for consumer in consumers:
        consumer.close_connection()
        consumer.join()  # Wait for threads to finish
    os._exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    consumers = [ConsumerThread() for _ in range(5)]
    try:
        for consumer in consumers:
            consumer.start()
    except Exception as e:
        print(f"Error: {e}")

