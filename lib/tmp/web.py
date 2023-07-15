import asyncio
import websockets

async def chat_server(websocket, path):
    async for message in websocket:
        await asyncio.gather(
            *[client.send(message) for client in clients],
            return_exceptions=True,
        )

async def main():
    async with websockets.serve(chat_server, "localhost", 8000):
        await asyncio.Future()  # run forever

clients = set()
asyncio.run(main())