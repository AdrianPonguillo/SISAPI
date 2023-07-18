import asyncio
import websockets
import random
import json
import socket
import threading
import time
import os

class Node:
    def __init__(self, name, ip, port, all_nodes):
        self.name = name
        self.ip = ip
        self.port = port
        self.all_nodes = all_nodes
        self.seed = random.randint(1000, 2000)
        self.is_leader = False
        self.server = None
        self.connections = {}
        self.seed_dict = {self.name: self.seed}
    
    async def who_iam(self):
        while True:
            if self.is_leader:
                i = 0
                while i < 5:                    
                    with open('files/COL0000272.json', 'r', encoding='iso-8859-1') as f:
                        enviar = {}
                        dato = json.loads(f.read())
                        try:
                            first_key = next(iter(dato))
                            
                            iper = dato[first_key]
                            #print(iper)
                            enviar['record'] = iper
                            jenviar = json.dumps(enviar)
                            #print(jenviar)

                            for ws in self.connections.values():
                                await ws.send(jenviar)
                                #print('Enviado registro')
                        except Exception as ex :
                            print(ex)
                        #print(enviar)
                        #print(iper['informacion_personal']['user_id'])
                        '''
                        for ws in self.connections.values():
                            ws.send(enviar)
                            print('Enviado registro')
                        '''
                        i = i + 1
                #print('ya no se enviara mas ...')
                time.sleep(5)

    async def start(self):
        def run_who_iam():
            asyncio.run(self.who_iam())
    
        start_server = websockets.serve(self.listen, self.ip, self.port)
        self.server = await start_server
        print(f"Node {self.name} started at {self.ip}:{self.port}")
        await self.connect_to_other_nodes()
        #print('Vemos si entra a send_seeds')
        await self.send_seeds()
        threading.Thread(target=run_who_iam).start()
        #for ws in self.connections.values():
        #    await ws.send('ping')
        #await self.send_record()

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()
        print(f"Node {self.name} stopped at {self.ip}:{self.port}")

    async def listen(self, websocket, path):
        try:
            ip = websocket.remote_address[0]
            if not any(node['ip'] == ip for node in self.all_nodes):
                # This IP is not in the list of nodes, so close the connection
                await websocket.close()
                return
            print(f"Connection established with {ip}")
            self.connections[ip] = websocket
            while True:
                message = await websocket.recv()
                #if message == "ping":
                #    await websocket.send("pong")
                #    print(f'Recibiendo ping desde {self.name}')
                #else:
                msg = json.loads(message)
                print(msg)
                if 'record' in msg:
                    record = msg['record']
                    print(f'Recibido en {self.name} : {record}')
                elif 'estado' in msg:
                    estado = msg['estado']
                    self.get_estado(estado)
                else:
                    # Merging received seed with local seed_dict
                    self.seed_dict.update(msg)                    
                    if len(self.seed_dict) == len(self.all_nodes) + 1:
                        print(f"Updated seed_dict: {self.seed_dict}")  # Printing updated seed_dict
                        self.determine_leader()
        except websockets.exceptions.ConnectionClosedError:
            print('Conexion cerrada inesperadamente')


    async def send_record(self):
        i = 0
        if self.is_leader:
            while i < 5:
                with open('files/COL0000272.json', 'r') as f:
                    for ws in self.connections.values():
                        json_x = {'record':json.loads(f.read())}
                        print(json_x)
                        await ws.send(json_x)
                i = i + 1

    async def get_estado(self, estado):
        print(estado)

    async def connect_to_other_nodes(self):
        async def connect_to_node(node):
            while True:
                try:
                    ws = await websockets.connect(f"ws://{node['ip']}:{node['port']}", ping_interval=None)
                    self.connections[node['ip']] = ws
                    print(f"Connected to {node['ip']}:{node['port']}")
                    break
                except ConnectionRefusedError:
                    print(f"Connection refused by {node['ip']}:{node['port']}, retrying in 5 seconds")
                    await asyncio.sleep(5)

        tasks = []
        for node in self.all_nodes:
            if node['ip'] != self.ip:
                tasks.append(asyncio.create_task(connect_to_node(node)))
        await asyncio.gather(*tasks)

    async def send_seeds(self):
        seed_message = json.dumps({self.name: self.seed})
        #print(seed_message)
        #print('generado seed_message')
        for ws in self.connections.values():
            #print('ws')
            await ws.send(seed_message)
            #print('envio message')

    async def check_leader(self):
        while self.is_leader:
            for ws in self.connections.values():
                await ws.send("ping")
                pong = await ws.recv()
                if pong != "pong":
                    print(f"A node did not respond. Choosing new leader.")
                    self.is_leader = False
                    self.leader = None
                    self.determine_leader()
            await asyncio.sleep(1)

    def determine_leader(self):
        leader_name = max(self.seed_dict, key=self.seed_dict.get)
        if self.name == leader_name:
            self.is_leader = True
            print(f"This node ({self.name}) is now the leader")
        else:
            print(f"The leader is {leader_name}")


