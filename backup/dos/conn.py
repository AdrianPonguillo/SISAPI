import asyncio
import websockets
import threading
import random
import json

class Node:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.seed = random.randint(1000, 2000)
        self.is_leader = False
        self.server = None
        self.websocket = None

class Cluster:
    def __init__(self, nodes):
        self.nodes = nodes
        self.leader = None
        self.leader_seed = None
        self.seed_dict = {}

    async def start_node(self, node):
        start_server = websockets.serve(self.listen, node.ip, node.port)
        node.server = await start_server
        print(f"Node {node.name} started at {node.ip}:{node.port}")

    async def stop_node(self, node):
        node.server.close()
        await node.server.wait_closed()
        print(f"Node {node.name} stopped at {node.ip}:{node.port}")

    async def listen(self, websocket, path):
        node = self.get_node_by_ip(websocket.remote_address[0])
        if node:
            print(f"Connection established with {node.name}")
            node.websocket = websocket
            while True:
                message = await websocket.recv()
                if message == "ping":
                    await websocket.send("pong")
                else:
                    seed = json.loads(message)
                    self.seed_dict.update(seed)
                    if len(self.seed_dict) == len(self.nodes):
                        self.determine_leader()

    async def send_seed(self, node, other_node):
        if node.websocket:
            await node.websocket.send(json.dumps({node.name: node.seed}))

    async def check_leader(self, node):
        while node.is_leader:
            if node.websocket:
                await node.websocket.send("ping")
                pong = await node.websocket.recv()
                if pong != "pong":
                    print(f"{node.name} did not respond. Choosing new leader.")
                    node.is_leader = False
                    self.leader = None
                    self.determine_leader()
            await asyncio.sleep(1)

    async def run(self, node):
        for other_node in self.nodes:
            if other_node != node:
                await self.send_seed(node, other_node)
        while not self.leader:
            await asyncio.sleep(1)
        if node.is_leader:
            await self.check_leader(node)

    def get_node_by_ip(self, ip):
        for node in self.nodes:
            if node.ip == ip:
                return node
        return None

    def determine_leader(self):
        leader_name = max(self.seed_dict, key=self.seed_dict.get)
        for node in self.nodes:
            if node.name == leader_name:
                node.is_leader = True
                self.leader = node
                print(f"Node {node.name} is now the leader")

import socket

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def main():
    nodes_info = [
        {'name': 'dist4', 'ip': '172.27.176.5', 'port': 8000},
        {'name': 'dist5', 'ip': '172.27.176.6', 'port': 8000},
        {'name': 'dist6', 'ip': '172.27.176.7', 'port': 8000},
        {'name': 'dist7', 'ip': '172.27.176.8', 'port': 8000},
    ]

    nodes = [Node(info['name'], info['ip'], info['port']) for info in nodes_info]
    cluster = Cluster(nodes)

    for node in nodes:
        print(node.name)
        threading.Thread(target=asyncio.run, args=(cluster.run(node),)).start()

if __name__ == "__main__":
    main()
    print('Se ha procesado main ... ')
