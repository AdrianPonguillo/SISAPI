import threading
import asyncio
import json
import websockets
import random
import time

class Node:
    def __init__(self, ip):
        self.ip = ip
        self.status = False
        self.name = "nodo" + str(random.randint(1000, 9999))

class NodeCommunication:
    def __init__(self, nodes):
        self.nodes = nodes
        self.statuses = {}

    async def send_message(self, node, message):
        try:
            async with websockets.connect(f"ws://{node.ip}:8765", timeout=5) as websocket:
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

    async def check_node_status(self, node):
        try:
            response = await asyncio.wait_for(self.send_message(node, "ping"), timeout=5)
            if response == "pong":
                node.status = True
            else:
                node.status = False
        except:
            node.status = False

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
            for other_node in self.nodes:
                if other_node != node:
                    await self.send_message(other_node, f"{node.name} {number}")
            await asyncio.sleep(5)

    async def run(self):
        async with websockets.serve(self.handle_message, "localhost", 8765):
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
    nodes = [Node("localhost"), Node("localhost")]
    node_communication = NodeCommunication(nodes)
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=lambda: asyncio.run(node_communication.run()))
    thread.start()

    while True:
        print(time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(20)