import asyncio
import websockets
import threading
import queue
import time

class Repository(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            message = self.client.received_messages.get()
            with open("respaldo.txt", "a") as file:
                file.write(message + "\n")
            asyncio.run(self.client.send("registro guardado"))
'''
class Client:
    def __init__(self):
        self.received_messages = queue.Queue()

    async def start(self):
        async with websockets.connect("ws://localhost:8765") as websocket:
            self.websocket = websocket
            self.repository = Repository(self)
            self.repository.start()
            while True:
                message = await websocket.recv()
                self.received_messages.put(message)

    async def send(self, message):
        await self.websocket.send(message)
'''

class Client:
    def __init__(self, host, port):
        self.uri = f"ws://{host}:{port}"
        self.connected = False

    async def connect(self):
        while not self.connected:
            try:
                self.websocket = await websockets.connect(self.uri)
                self.connected = True
            except ConnectionRefusedError:
                print("Conexión rechazada. Reintentando en 5 segundos...")
                await asyncio.sleep(5)

    async def send_message(self, message):
        if not self.connected:
            await self.connect()
        await self.websocket.send(message)

    async def receive_message(self):
        if not self.connected:
            await self.connect()
        message = await self.websocket.recv()
        return message


client = Client('localhost', 8765)


while True:
    try:
        asyncio.get_event_loop().run_until_complete(client.start())
        break  # Si la conexión se establece correctamente, se sale del bucle.
    except websockets.exceptions.ConnectionClosedError:
        print("La conexión con el servidor se cerró inesperadamente. Intentando reconectar en 5 segundos...")
        time.sleep(5)  # Espera un poco antes de intentar de nuevo.