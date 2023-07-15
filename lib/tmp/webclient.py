import asyncio
import websockets
import time

'''
async def enviar_solicitud(cadena):
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(cadena)
        cadena_invertida = await websocket.recv()
        print(f"Cadena invertida recibida: {cadena_invertida}")

async def cliente():
    while True:
        cadena = input("Ingrese una cadena: ")
        await enviar_solicitud(cadena)

asyncio.run(cliente())
'''


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def send_message(self, message):
        inicio = time.time()
        async with websockets.connect(f"ws://{self.host}:{self.port}") as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Recibido {response!r}")
        fin = time.time()
        return self.host+':'+str(self.port), (fin - inicio) 

def servidor_mas_rapido(servidores):
    servidor_mas_rapido = None
    tiempo_mas_rapido = float("inf")
    for servidor, tiempo in servidores.items():
        if tiempo < tiempo_mas_rapido:
            servidor_mas_rapido = servidor
            tiempo_mas_rapido = tiempo
    return servidor_mas_rapido, tiempo_mas_rapido



servidores = [{'server': 'localhost', 'port': 8080}, 
              {'server': 'localhost', 'port': 8081},
              {'server': 'localhost', 'port': 8082},
              {'server': 'localhost', 'port': 8083},
              ]

tiempos = {}

if __name__ == "__main__":
    async def run_client():
        client1 = Client("localhost", 8888)
        serv, r = await client1.send_message("Hola, servidor!1")
        tiempos[serv + '1'] = r
        print('Demorado {0}'.format(r))
        serv, r = await client1.send_message("Hola, servidor!2")
        tiempos[serv + '2'] = r
        print('Demorado {0} {1}'.format(serv, r))
        serv, r = await client1.send_message("Hola, servidor!3")
        tiempos[serv + '3'] = r
        print('Demorado {0} {1}'.format(serv, r))


asyncio.run(run_client())
print(tiempos)

servidor, tiempo = servidor_mas_rapido(tiempos)
print(f"El servidor más rápido es {servidor} con un tiempo de {tiempo} segundos")