import asyncio
import websockets

class SocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        while self.websocket is None:
            try:
                self.websocket = await websockets.connect(self.uri)
            except ConnectionRefusedError:
                print("Connection refused, retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def start(self):
        while True:
            try:
                if self.websocket is None or self.websocket.closed:
                    await self.connect()
                while True:
                    message = await self.websocket.recv()
                    print(f"< {message}")
                    await self.websocket.send('pruban')
                    await asyncio.sleep(1)
            except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
                print("Connection lost, trying to reconnect...")
                self.websocket = None

    async def send_message(self, message):
        if self.websocket is None or self.websocket.closed:
            await self.connect()
        await self.websocket.send(message)

    async def close(self):
        if self.websocket is not None:
            await self.websocket.close()

if __name__ == '__main__':
    client = SocketClient('ws://localhost:8765')
    asyncio.get_event_loop().run_until_complete(client.start())
