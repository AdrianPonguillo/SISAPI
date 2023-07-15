import asyncio
import websockets
import queue
import time

class Server:
    connected_clients = set()

    def __init__(self, host, port, mqueue):
        self.host = host
        self.port = port
        self.message_queue = mqueue
        #print(mqueue)
        self.start_server = websockets.serve(self.client_handler, host, port)

    async def client_handler(self, websocket, path):
        # Añadir el nuevo cliente a la lista de clientes conectados
        self.connected_clients.add(websocket)
        try:
            # Bucle principal del servidor
            while True:
                # Comprobar si hay mensajes en la cola
                if not self.message_queue.empty():
                    message = self.message_queue.get()

                    # Enviar el mensaje a todos los clientes conectados
                    await asyncio.gather(
                        *[client.send(message) for client in connected_clients],
                        return_exceptions=True,
                    )
                    print('enviado c {0}'.format(message))
                    
                    # Espera respuesta de todos los clientes
                    responses = await asyncio.gather(
                        *[client.recv() for client in connected_clients],
                        return_exceptions=True,
                    )
                    
                    # Verifica si todas las respuestas son "1"
                    if all(response == "1" for response in responses):
                        continue
                    else:
                        self.message_queue.put(message)  # Vuelve a poner el mensaje en la cola

                time.sleep(5)
                await asyncio.sleep(0.1)
        finally:
            # Si un cliente se desconecta, lo eliminamos de la lista de clientes conectados
            connected_clients.remove(websocket)
        



# La cola de mensajes a enviar
message_queue = queue.Queue()

connected_clients = set()

def generate_primes(n):
    primes = []
    i = 2
    while len(primes) < n:
        if all(i % prime != 0 for prime in primes):
            primes.append(i)
        i += 1
    return primes


# Generar los primeros 20 números primos y agregarlos a la cola
primes = generate_primes(20)
for prime in primes:
    message_queue.put(str(prime))

server = Server('localhost', '8765', message_queue)

asyncio.get_event_loop().run_until_complete(server.start_server)
asyncio.get_event_loop().run_forever()