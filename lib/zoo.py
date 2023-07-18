from kazoo.client import KazooClient, KazooState
from kazoo.recipe.lock import Lock
from kazoo.exceptions import KazooException, NoNodeError
from kazoo.protocol.states import WatchedEvent
import json
import os
import time
import logging
import requests
from  lib.repository import Repository

logging.basicConfig()


class Node:
    def __init__(self, hosts='172.20.198.207:2181', endpoint='http://20.55.70.215:8080/get_file'):
        self.zk = KazooClient(hosts=hosts)
        self.leader_lock = self.zk.Lock("/leader")
        self.is_leader = False
        self.endpoint = endpoint
        self.repository = Repository()
        self.partitions = {}
        self.partitions = self.repository.get_index()

    def connect(self):
        for _ in range(50):  # Hacer 50 intentos de conexión.
            try:
                self.zk.start()
                break
            except KazooException:
                time.sleep(5)  # Esperar un poco antes de intentar de nuevo.

    def run_for_leadership(self):
        while True:
            try:
                self.is_leader = self.leader_lock.acquire(blocking=False)
                if self.is_leader:
                    self.handle_data()
                else:
                    self.listen_for_data()
            except KazooException:
                self.is_leader = False
                time.sleep(5)  # Esperar un poco antes de intentar de nuevo.

    def handle_data(self):
        data = self.get_data()
        if data:
            self.repository.set_data(data)
            if self.repository.save_data(self.partitions) != 1:
                print("Hubo un problema al guardar los datos en el nodo líder")
            else:
                self.distribute_data(data)

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
            self.zk.set(data_node_path, data_str.encode())
        else:
            self.zk.create(data_node_path, data_str.encode())
    
    def listen_for_data(self):
        data_node_path = "/data"
        try:
            data, stat = self.zk.get(data_node_path, watch=self.data_watch)
            self.handle_received_data(data)
        except NoNodeError:
            pass  # El nodo de datos aún no existe.

    def data_watch(self, event: WatchedEvent):
        if event.type == "CHANGED":
            self.listen_for_data()  # Volver a escuchar para actualizar los datos.

    def handle_received_data(self, data):
        data_json = json.loads(data.decode())
        self.repository.set_data(data_json)
        if self.repository.save_data(self.partitions) != 1:
            print(f"Hubo un problema al guardar los datos en el nodo {self.zk.client_id}")


'''

partitions = {}

repos = Repository()
#repos.regenerate_index(partitions)
partitions = repos.get_index()
#print(partitions)


for i in range(0,1000):
    user_id = 'clave' + str(i)
    data = {'user_id': user_id, 'name': 'Juan perez cando', 'age': 30}
    
    repos.set_data(data)
    r = repos.save_data(partitions)
    print('Procesado {0} insertado {1}'.format(i,r))


Repository().save_index(partitions)    
#clave9878
#clave9193

print(repos.read_data('clave838', partitions))
print(repos.read_data('clave190', partitions))
print(repos.read_data('clave115', partitions))
#print(partitions)'''