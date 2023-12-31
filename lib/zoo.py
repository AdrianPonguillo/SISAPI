from kazoo.client import KazooClient, KazooState
from kazoo.recipe.lock import Lock
from kazoo.exceptions import KazooException, NoNodeError
from kazoo.protocol.states import WatchedEvent
import json
import time
import logging
import requests
from  lib.repository import Repository

logging.basicConfig()

class Node:
    """
    Clase que crea los nodos del sistema, se conecta entre ellos y envia y controla la transacción distribuida en la base de datos

    Atributos:
        self.zk: Nodo
        self.leader_lock: Define quien es el lider bloqueando a todos los nodos
        self.is_leader: Para preguntar quien es el lider
        self.endpoint: Url api 'http://20.55.70.215:8080/get_file'
        self.repository: Base de datos del sistema
        self.partitions: Indice en memoria para la base de datos
        self.latest_data: Atributo para guardar los últimos datos distribuidos por el nodo líder

    Métodos:
        __init__(hosts, endpoint): Inicializacion de parametros del sistema
        connect(): Conexión y creación de nodos, se realizan 50 intentos sino el sistema no entra
        run_for_leadership(): Corre la lógica del producto, verifica quien es el lider y le entrega la tarea de conectarse 
                            al endpoint y enviar la data a los nodos seguidores. Trabaja cuando hay al menos 3 nodos conectados
        handle_data(): Maneja la transacción en la base de datos, guarda el dato y guarda el indice. Si esta guardado envia a los demas nodos
        get_data(): Conexión con el endpoint para traer los datos del servidor de archivos de formularios
        distribute_data(data): Envia el dato a todos los nodos del sistema
        listen_for_data(): En los nodos seguidores se encarga de atender la data recibida
        data_watch(data, stat, event): Watch del modulo, maneja el criterio de seguir o detenerse en caso de que algo cambie
        handle_received_data(data): Se encarga de almacenar en los nodos seguidores los datos
        close(): Controla el cierre de la conexión de los datos 
    """

    def __init__(self, hosts='172.20.198.207:2181', endpoint='http://20.55.70.215:8080/get_file'):
        self.zk = KazooClient(hosts=hosts)
        self.leader_lock = self.zk.Lock("/leader")
        self.is_leader = False
        self.endpoint = endpoint
        self.repository = Repository() #Base de datos del sistema
        self.partitions = {}
        self.partitions = self.repository.get_index()
        self.latest_data = None  # Atributo para guardar los últimos datos distribuidos por el nodo líder

    def connect(self):
        for _ in range(50):  # Hacer 50 intentos de conexión.
            print(f'Intento {_+1}')
            try:
                self.zk.start()
                if not self.zk.exists("/nodes"):
                    self.zk.create("/nodes")
                node_path = self.zk.create("/nodes/node_", ephemeral=True, sequence=True)  # Crea un znode para este nodo
                #logging.info(f'Nodo conectado desde {self.zk.client.host}, ruta del nodo: {node_path}')
                break
            except KazooException as e:
                logging.error(f'Error de conexión en el intento {_+1}: {str(e)}')
                time.sleep(5)  # Esperar un poco antes de intentar de nuevo.

    def run_for_leadership(self):
        # Establecer watcher para el nodo de datos al principio
        data_node_path = "/data"
        if self.zk.exists(data_node_path):
            self.zk.DataWatch(data_node_path, self.data_watch)
        while True:
            try:
                # Verifica que hay al menos 3 nodos conectados antes de intentar adquirir el liderazgo
                if len(self.zk.get_children("/nodes")) < 3:
                    print("Esperando a que haya al menos 3 nodos conectados...")
                    time.sleep(10)
                    continue                
                self.is_leader = self.leader_lock.acquire(blocking=False)
                if self.is_leader:
                    print('Soy el lider....')
                    data = self.get_data()                    
                    if data:
                        self.latest_data = data
                        self.handle_data()
                        #time.sleep(3)
                    else:
                        break
                        # Aquí debes liberar el liderazgo para que otro nodo pueda tomar el control y distribuir nuevos datos.
                    self.leader_lock.release()
                    self.is_leader = False
                    #time.sleep(3)
                else:
                    self.listen_for_data()
                    #time.sleep(3)
            except KazooException:
                self.is_leader = False
                #time.sleep(3)  # Esperar un poco antes de intentar de nuevo.

    def handle_data(self):
        self.repository.set_data(self.latest_data)
        re = self.repository.save_data(self.partitions)
        self.repository.save_index(self.partitions)
        if  re == 0:
            print("Hubo un problema al guardar los datos en el nodo líder")
        elif re == 1:
            self.distribute_data(self.latest_data)
            #time.sleep(3)  # Esperar 5 segundos antes del siguiente guardado

    def get_data(self):
        try:
            response = requests.get(self.endpoint)
            data = response.json()
            return data
        except Exception as ex:
            print('Se ha producido un error:' + str(ex))
            return False

    def distribute_data(self, data):
        data_node_path = "/data"
        data_str = json.dumps(data)
        if self.zk.exists(data_node_path):
            current_data, stat = self.zk.get(data_node_path)
            if current_data.decode() != data_str:  # Sólo cambiar los datos si son diferentes
                self.zk.set(data_node_path, data_str.encode())
        else:
            self.zk.create(data_node_path, data_str.encode())

    def listen_for_data(self):
        data_node_path = "/data"
        try:
            data, stat = self.zk.get(data_node_path)
            if data != self.latest_data:
                self.handle_received_data(data)
        except NoNodeError:
            pass  # El nodo de datos aún no existe.

    def data_watch(self, data, stat, event: WatchedEvent):
        if event is not None and event.type == "CHANGED":
            self.listen_for_data()  # Volver a escuchar para actualizar los datos.

    def handle_received_data(self, data):
        try:
            data_json = json.loads(data.decode())
            self.repository.set_data(data_json)
            re = self.repository.save_data(self.partitions)
            self.repository.save_index(self.partitions)
            if  re == 0:
                print("Hubo un problema al guardar los datos en el nodo {self.zk.client_id}")
        except Exception as ex:
            print('Error: '+ str(ex))

    def close(self):
        if self.zk.connected:
            self.zk.stop()
            self.zk.close()


