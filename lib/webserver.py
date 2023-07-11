import asyncio
import websockets
import datetime

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        #self.start()
        print('Server creado')

    async def handle_client(self, websocket, path):
        #message = await websocket.recv()
        #print(f"Recibido {message!r}")
        #await websocket.send(message[::-1])
        # Enviar la hora actual a los clientes cada segundo
        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            await websocket.send(now)
            await asyncio.sleep(1)

    async def start(self):
        # Crear el servidor WebSocket
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        # Esperar a que el servidor se cierre
        await self.server.wait_closed()
        '''
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        async with self.server:
            await self.server.wait_closed()
        '''

    def stop(self):
        # Detener el servidor WebSocket
        if self.server:
            self.server.close()



'''

if __name__ == "__main__":
    async def run_server1():
        server1 = Server("localhost", 8888)
        await server1.start()
    

asyncio.run(run_server1())
'''