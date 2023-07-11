import asyncio
import time
import websockets

class Node:
    def __init__(self, name, ip, port_in, port_out):
        self.name = name
        self.ip = ip
        self.port_in = port_in
        self.port_out = port_out
        self.servers = {}
        self.times = {}

    async def handle_client(self, websocket, path):
        # Manejar conexiones WebSocket
        message = await websocket.recv()
        if message == 'estoy vivo':
            await websocket.send('estoy vivo')

    async def connect(self, ip, port):
        # Conectar al servidor WebSocket en el nodo remoto
        uri = f'ws://{ip}:{port}'
        async with websockets.connect(uri) as websocket:
            # Enviar un mensaje de "estoy vivo" y medir el tiempo de respuesta
            start_time = time.time()
            await websocket.send('estoy vivo')
            response = await websocket.recv()
            end_time = time.time()

            # Almacenar la duración de la respuesta en el diccionario de tiempos
            duration = end_time - start_time
            self.times[ip] = duration

    async def start(self):
        # Crear los servidores WebSocket
        for node in nodes:
            if node.ip != self.ip:
                uri = f'ws://{node.ip}:{node.port_in}'
                server = await websockets.serve(self.handle_client, self.ip, self.port_out)
                self.servers[node.ip] = server

        # Conectar a los otros nodos y medir los tiempos de respuesta
        tasks = []
        for node in nodes:
            if node.ip != self.ip:
                task = asyncio.create_task(self.connect(node.ip, node.port_out))
                tasks.append(task)
        await asyncio.gather(*tasks)

        # Imprimir los tiempos de respuesta
        print(self.times)

    async def stop(self):
        # Detener los servidores WebSocket
        for server in self.servers.values():
            server.close()
        await asyncio.gather(*self.servers.values())

nodes = [
    Node('dist4', '172.27.182.65', 888, 999),
    Node('dist5', '172.27.188.147', 888, 999),
    Node('dist6', '172.27.186.190', 888, 999),
    Node('dist7', '172.27.188.30', 888, 999)
]

async def main():
    # Iniciar los nodos
    tasks = []
    for node in nodes:
        task = asyncio.create_task(node.start())
        tasks.append(task)
    await asyncio.gather(*tasks)

    # Los nodos están en ejecución
    # ...

    # Detener los nodos
    tasks = []
    for node in nodes:
        task = asyncio.create_task(node.stop())
        tasks.append(task)
    await asyncio.gather(*tasks)

# Ejecutar el programa principal
asyncio.run(main())