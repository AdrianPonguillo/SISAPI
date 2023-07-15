'''
import asyncio
import websockets


async def invertir(cadena):
    return cadena[::-1]

async def procesar_solicitud(websocket, path):
    cadena = await websocket.recv()
    cadena_invertida = await invertir(cadena)
    print(f"Cadena invertida: {cadena_invertida}")
    await websocket.send(cadena_invertida)

async def servidor():
    async with websockets.serve(procesar_solicitud, "localhost", 8765):
        await asyncio.Future()  # Mantener el servidor en ejecución

asyncio.run(servidor())

import asyncio
import websockets
import time


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    async def handle_client(self, websocket, path):
        message = await websocket.recv()
        print(f"Recibido {message!r}")
        #await websocket.send(message[::-1])
        await websocket.send('Recibido ...')

    async def start(self):
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        async with self.server:
            await self.server.wait_closed()


if __name__ == "__main__":
    async def run_server1():
        server1 = Server("localhost", 8888)
        await server1.start()
    
    #async def run_server2():
    #    server2 = Server("localhost", 9999)
    #    await server2.start()

asyncio.run(run_server1())
#asyncio.run(run_server2())

'''


import asyncio
import websockets

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.clientes = []

    async def handle_client(self, websocket, path):
        self.clientes.append(websocket)
        try:
            while True:
                message = await websocket.recv()
                print(f"Recibido {message!r}")
                for cliente in self.clientes:
                    await cliente.send(message)
        finally:
            self.clientes.remove(websocket)

    async def start(self):
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        async with self.server:
            await self.server.wait_closed()

if __name__ == "__main__":
    async def run_server():
        server = Server("localhost", 8888)
        await server.start()

    asyncio.run(run_server())