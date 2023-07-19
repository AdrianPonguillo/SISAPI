from  threading import Thread
import threading
import json
import os
from lib.conexion import Conexion
import signal

class Repositorio(Thread):
    """
    Clase que almacena los datos obtenidos de la cola de mensajes en un repositorio del servidor
      
    Métodos:
        __init__(): Constructor de la clase
        run(user_id, contenido): Guarda los datos obtenidos en ficheros con extensión json
        launch_tasks(n): Genera los n hilos de la clase
    """
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
    """
    Clase que se conecta a RabbitMQ y envia los datos a la clase Repositorio para ser almacenados
    
    Atributos:
        file_lock: Bloqueo de hilos

    Métodos:
        __init__(): Constructor de la clase
        close_connection(): Controla el cierre de la conexión con RabbitMQ
        launch_tasks(n): Genera los n hilos de la clase
        callback(ch, method, properties, body): Controla el flujo de mensajes en la cola
        run(): Crea el hilo de ejecución
        signal_handler: Gestiona la interacción con el usuario por teclado
    """
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

