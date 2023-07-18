import asyncio
import websockets
import os
import json
from threading import Thread
import socket

nodes_info = [
    {'name': 'dist4', 'ip': '172.27.176.5', 'port': 8000},
    {'name': 'dist5', 'ip': '172.27.176.6', 'port': 8001},
    {'name': 'dist6', 'ip': '172.27.176.7', 'port': 8002},
    {'name': 'dist7', 'ip': '172.27.176.8', 'port': 8003},
]

class Node:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.online = False
        self.is_leader = False
        self.websocket = None

    async def connect(self):
        while not self.online:
            try:
                self.websocket = await websockets.connect(f'ws://{self.ip}:{self.port}')
                self.online = True
                print(f'Conectado a {self.name}')
            except Exception as e:
                print(f'Fallo al conectar a {self.name}, reintentando. Error: {e}')
                await asyncio.sleep(1)

    async def start_server(self):
        async def echo(websocket, path):
            async for message in websocket:
                print(f"Recibido: {message}")

        server = websockets.serve(echo, self.ip, self.port)
        await server


class Server:
    def __init__(self, nodes_info):
        self.nodes = [Node(**node_info) for node_info in nodes_info]
        self.nodes[0].is_leader = True

    def get_current_node(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return next((node for node in self.nodes if node.ip == ip_address), None)

    def start_connections(self):
        current_node = self.get_current_node()
        if current_node:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(current_node.start_server())

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [node.connect() for node in self.nodes if node != current_node]
        loop.run_until_complete(asyncio.gather(*tasks))

    def notify_all(self, message):
        for node in self.nodes:
            if node.online:
                asyncio.run(node.websocket.send(message))

    def sense_nodes(self):
        while True:
            for node in self.nodes:
                if node.online and node.websocket.open == False:
                    node.online = False
                    print(f"El nodo {node.name} ya no se encuentra en línea.")
                    self.notify_all(f"El nodo {node.name} ya no se encuentra en línea.")

    def send_files(self):
        for file in os.listdir('../files'):
            if file.endswith('.json'):
                with open(f'../files/{file}', 'r') as f:
                    data = json.load(f)
                    self.notify_all(data)

    def run(self):
        self.start_connections()

        sensing_thread = Thread(target=self.sense_nodes)
        sensing_thread.start()

        send_files_thread = Thread(target=self.send_files)
        send_files_thread.start()

server = Server(nodes_info)
server.run()
