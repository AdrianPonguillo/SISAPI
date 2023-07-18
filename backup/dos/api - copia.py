import asyncio
import websockets
import random
import json
import socket
import datetime

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

    async def start(self):
        start_server = websockets.serve(self.listen, self.ip, self.port)
        self.server = await start_server
        print(f"Node {self.name} started at {self.ip}:{self.port}")
        await self.connect_to_other_nodes()
        await asyncio.sleep(5) 
        await self.send_seeds()
        if self.is_leader:
            #self.message_repository()
            self.send_user_input()

    async def send_user_input(self):
        while True:
            user_input = input('Enter a message: ')
            await self.broadcast_message(user_input)

    async def message_repository(self):
        while self.is_leader:
            current_time = datetime.datetime.now()
            message = 'La hora actual es ' + current_time.strftime("%H:%M:%S")
            await self.broadcast_message(message)
            await asyncio.sleep(1)

    async def broadcast_message(self, message):
        for ws in self.connections.values():
            await ws.send(message)

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()
        print(f"Node {self.name} stopped at {self.ip}:{self.port}")

    async def listen(self, websocket, path):
        ip = websocket.remote_address[0]
        if not any(node['ip'] == ip for node in self.all_nodes):
            await websocket.close()
            return
        print(f"Connection established with {ip}")
        self.connections[ip] = websocket
        while True:
            message = await websocket.recv()
            if message.startswith("La hora actual es"):
                print(message)
            elif self.is_leader and message == "ping":
                await websocket.send("pong")
            elif not self.is_leader and not message.startswith("La hora actual es"):
                reversed_message = message[::-1]   # reverse the message
                await websocket.send(reversed_message)  # send reversed message
            else:
                seed = json.loads(message)
                self.seed_dict.update(seed)
                print(f"Updated seed_dict: {self.seed_dict}")  
                if len(self.seed_dict) == len(self.all_nodes):
                    self.determine_leader()
    
    async def connect_to_other_nodes(self):
        async def connect_to_node(node):
            while True:
                try:
                    ws = await websockets.connect(f"ws://{node['ip']}:{node['port']}", timeout=20.0)
                    self.connections[node['ip']] = ws
                    print(f"Connected to {node['ip']}:{node['port']}")
                    break
                except (ConnectionRefusedError, asyncio.exceptions.TimeoutError):
                    print(f"Connection refused by {node['ip']}:{node['port']}, retrying in 5 seconds")
                    await asyncio.sleep(5)

        connection_tasks = [connect_to_node(node) for node in self.all_nodes if node['ip'] != self.ip]
        await asyncio.gather(*connection_tasks)

    async def send_seeds(self):
        seed_message = json.dumps({self.name: self.seed})
        for ws in self.connections.values():
            await ws.send(seed_message)

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



def main():
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    nodes_info = [
        {'name': 'dist4', 'ip': '172.27.176.5', 'port': 8000},
        {'name': 'dist5', 'ip': '172.27.176.6', 'port': 8000},
        {'name': 'dist6', 'ip': '172.27.176.7', 'port': 8000},
        {'name': 'dist7', 'ip': '172.27.176.8', 'port': 8000},
        #{'name': 'dist8', 'ip': '172.28.252.102', 'port': 8000},
    ]

    def get_hostname(ip):
        for node in nodes_info:
            if node['ip'] == ip:
                print(node)
                return node
        return None 

    local_ip = get_local_ip()
    print(local_ip)
    current_node_info = get_hostname(local_ip)
    node_name = current_node_info['name']
    node_port = current_node_info['port']

    node = Node(node_name, local_ip, node_port, nodes_info)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(node.start())
    loop.run_forever()

if __name__ == "__main__":
    main()




