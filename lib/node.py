import socket
import random
import threading
import asyncio
import json
import websockets
import random
import time

class Host:

    nodos = [
        {'name': 'dist4', 'ip':'172.27.176.5', 'porta': 8000, 'portb': 9000},
        {'name': 'dist5', 'ip':'172.27.176.6', 'porta': 8000, 'portb': 9000},
        {'name': 'dist6', 'ip':'172.27.176.7', 'porta': 8000, 'portb': 9000},
        {'name': 'dist7', 'ip':'172.27.176.8', 'porta': 8000, 'portb': 9000},
        #{'name': 'dist8', 'ip':'172.28.252.102', 'porta': 8000, 'portb': 9000},
    ]

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
        
    def get_hostname(self, ip):
        for node in self.nodos:
            if node['ip'] == ip:
                print(node)
                return node
        return None
    
    def get_other_ips(self):
        other = []
        for i in self.nodos:
            if i['ip'] != self.get_local_ip():
                other.append(i)
        #print(other)
        return other
    

class Node:
    def __init__(self, ip ):
            self.ip = ip
            self.localhost = Host().get_hostname(self.ip)
            self.status = False
            self.name = self.localhost['name']    
            self.port = self.localhost['porta']        

    def set_value(self, value):
        self.value = value


class SharedObject:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}

    def update(self, node_name, value):
        with self.lock:
            self.data[node_name] = value

    def get_data(self):
        with self.lock:
            return self.data.copy()


class NodeCommunication:
    def __init__(self, nodes):
        self.nodes = nodes
        self.statuses = {}
        self.shared_object = SharedObject()
    
    def get_shared_data(self):
        return self.shared_object.get_data()

    async def send_message(self, node, message):
        try:
            async with websockets.connect(f"ws://{node.ip}:{node.port}", timeout=5) as websocket:
                await websocket.send(message)
                response = await websocket.recv()
                return response
        except websockets.exceptions.ConnectionClosedOK:
            print(f"Error: La conexión con {node.ip} se cerró inesperadamente.")
            return None
        except asyncio.TimeoutError:
            print("Esperando nodos para conectarse...")
            await asyncio.sleep(5)
            return None
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar con {node.ip}. Reintentando en 5 segundos...")
            await asyncio.sleep(5)
            return None
    
    async def check_node_status(self, node):
        try:
            response = await asyncio.wait_for(self.send_message(node, "ping"), timeout=5)
            if response == "pong":
                node.status = True
            else:
                node.status = False
        except websockets.exceptions.ConnectionClosedError as e:
            if e.code == 1006:
                print(f"Error: No se pudo conectar con {node.ip}. Reintentando en 5 segundos...")
            else:
                print(f"Error: La conexión con {node.ip} se cerró inesperadamente.")
            node.status = False
        except asyncio.TimeoutError:
            print("Esperando nodos para conectarse...")
            node.status = False
            await asyncio.sleep(5)
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar con {node.ip}. Reintentando en 5 segundos...")
            node.status = False
            await asyncio.sleep(5)

    async def check_nodes_statuses(self):
        tasks = []
        for node in self.nodes:
            task = asyncio.ensure_future(self.check_node_status(node))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def send_random_number(self, node):
        while True:
            number = random.randint(1000, 2000)
            print(f"{node.name}: Envie {number}")
            self.shared_object.update(node.name, number)  # Actualizar el objeto compartido
            for other_node in self.nodes:
                if other_node != node:
                    await self.send_message(other_node, f"{node.name} {number}")
            await asyncio.sleep(5)

    async def run(self, node):
        print('Soy {0}'.format(node.name))
        async with websockets.serve(self.handle_message, node.ip, node.port):
            for node in self.nodes:
                await asyncio.create_task(self.send_random_number(node))
            while True:
                await self.check_nodes_statuses()
                self.statuses = {node.ip: node.status for node in self.nodes}
                await asyncio.sleep(20)

    async def handle_message(self, websocket, path):
        message = await websocket.recv()
        sender_name, number = message.split()
        print(f"Recibi de {sender_name} el numero {number}")


if __name__ == "__main__":
    hosts = Host()
    other_ips = hosts.get_other_ips()
    server = Node(hosts.get_local_ip())
    other_nodos = []
    for oi in other_ips:
        other_nodos.append(Node(oi['ip']))

    node_communication = NodeCommunication(other_nodos)
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=lambda: asyncio.run(node_communication.run(server)))
    thread.start()

    while True:
        print(time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(20)
        shared_data = node_communication.get_shared_data()
        print("Datos compartidos:")
        for node_name, value in shared_data.items():
            print(f"{node_name}: {value}")



