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
        self.websocket = None

    async def handle_server(self, websocket, path):
        # Manejar conexiones WebSocket
        self.websocket = websocket
        while True:
            # Recibir mensajes del servidor
            message = await self.websocket.recv()
            print(f'Mensaje recibido: {message}')

    async def start(self):
        # Conectar al servidor WebSocket
        uri = f'ws://{self.ip}:{self.port_in}'
        async with websockets.connect(uri) as websocket:
            # Manejar conexiones WebSocket
            await self.handle_server(websocket, uri)

            # Esperar a que el usuario ingrese un mensaje
            while True:
                message = input('Ingrese un mensaje: ')
                await self.websocket.send(message)

# Crear los nodos
nodes = [
    {'name': 'dist4', 'ip':'172.27.182.65',  'port-in': 8000, 'port-out': 9000},
    {'name': 'dist5', 'ip':'172.27.188.147', 'port-in': 8000, 'port-out': 9000},
    {'name': 'dist6', 'ip':'172.27.186.190', 'port-in': 8000, 'port-out': 9000},
    {'name': 'dist7', 'ip':'172.27.188.30',  'port-in': 8000, 'port-out': 9000},
]

# Obtener la dirección IP del equipo
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Crear el servidor y el cliente WebSocket
server = None
client = None

if ip_address == '172.27.182.65':
    server = WebSocketServer('172.27.182.65', 8000, 9000)
elif ip_address == '172.27.188.147':
    client = WebSocketClient('172.27.182.65', 9000, 8000)

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