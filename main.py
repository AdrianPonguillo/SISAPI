import lib.webclient
import lib.webserver as srv
import lib.ip_config as ip
import socket
import asyncio 
import datetime
import websockets

def get_infonet():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

def remove_dict_by_ip(lst, ip):
    result = []
    for d in lst:
        if d['ip'] != ip:
            result.append(d)
    return result

lista_server = remove_dict_by_ip(ip.nodos, '172.27.188.147')

async def handler(websocket, path):
    # Enviar la hora actual a los clientes cada segundo
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(1)


async def main():
    for s in lista_server:
        print(s)
        #async def run_server():
        server = srv.Server(s['ip'], s['port-in'])
        await server.start()
        #async with websockets.serve(handler, s['ip'], s['port-in']):
            # Esperar a que el servidor se cierre
            #await asyncio.Future()
        server.stop()

asyncio.run(main())

'''

if __name__ == "__main__":
    async def run_server1():
        server1 = Server("localhost", 8888)
        await server1.start()
    

asyncio.run(run_server1())
'''

#print(lista_server)

#print(ip.nodos)


