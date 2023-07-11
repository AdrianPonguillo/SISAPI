import asyncio
import datetime
import websockets
import socket

class WebSocketServer:
    def __init__(self, ip, port_in, port_out):
        self.ip = ip
        self.port_in = port_in
        self.port_out = port_out
        self.server = None

    async def handle_client(self, websocket, path):
        # Manejar conexiones WebSocket
        while True:
            # Enviar la hora actual al cliente
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await websocket.send(now)

            # Esperar 5 segundos antes de enviar la siguiente hora
            await asyncio.sleep(5)

    async def start(self):
        # Crear el servidor WebSocket
        uri = f'ws://{self.ip}:{self.port_in}'
        self.server = await websockets.serve(self.handle_client, self.ip, self.port_out)

        # Mantener el servidor WebSocket en ejecución
        await self.server.wait_closed()

    async def stop(self):
        # Detener el servidor WebSocket
        if self.server:
            self.server.close()
            await self.server.wait_closed()

class WebSocketClient:
    def __init__(self, ip, port_in, port_out):
        self.ip = ip
        self.port_in = port_in
        self.port_out = port_out

    async def handle_server(self, websocket, path):
        # Manejar conexiones WebSocket
        while True:
            # Recibir la hora actual del servidor
            now = await websocket.recv()
            print(f'Hora actual: {now}')

    async def start(self):
        # Conectar al servidor WebSocket
        uri = f'ws://{self.ip}:{self.port_in}'
        async with websockets.connect(uri) as websocket:
            # Manejar conexiones WebSocket
            await self.handle_server(websocket, uri)

# Crear los nodos
nodes = [
    {'name': 'dist4', 'ip':'172.27.182.65',  'port-in': 8000, 'port-out': 9000},
    {'name': 'dist5', 'ip':'172.27.188.147', 'port-in': 8000, 'port-out': 9000},
    {'name': 'dist6', 'ip':'172.27.186.190', 'port-in': 8000, 'port-out': 9000},
    {'name': 'dist7', 'ip':'172.27.188.30',  'port-in': 8000, 'port-out': 9000},
]

def get_infonet():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

hostname , ip_address = get_infonet()


if ip_address == '172.27.182.65':
    server = WebSocketServer(ip_address, 8000, 9000)
elif ip_address == '172.27.188.147':
    client = WebSocketClient(ip_address, 8000, 9000)

# Iniciar el servidor y el cliente WebSocket
async def main():
    tasks = []
    if server:
        task = asyncio.create_task(server.start())
        tasks.append(task)
    if client:
        task = asyncio.create_task(client.start())
        tasks.append(task)
    await asyncio.gather(*tasks)

# Ejecutar el programa principal
asyncio.run(main())