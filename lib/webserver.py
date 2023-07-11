import asyncio
import websockets

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    async def handle_client(self, websocket, path):
        message = await websocket.recv()
        print(f"Recibido {message!r}")
        await websocket.send(message[::-1])

    async def start(self):
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        async with self.server:
            await self.server.wait_closed()

'''

if __name__ == "__main__":
    async def run_server1():
        server1 = Server("localhost", 8888)
        await server1.start()
    

asyncio.run(run_server1())
'''