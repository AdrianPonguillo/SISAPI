from lib.config import Config
from lib.node import Node 
from lib.comunica import ServerSocket, ClientSocket
import socket
import time

config = Config('config.ini')
#nodes = config.get_nodes()
nodes = config.get_ips()

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

self_ip = get_private_ip() 
#self_ip = '10.2.0.5'


print(nodes)
print('*'*40)

# Crear la lista de direcciones de nodos
#node_addresses = list(nodes.values())

l = []
print(self_ip)

for node_name, node_address in nodes.items():
    if node_address != self_ip:
        l.append(node_address)


print(l)

server = ServerSocket(self_ip)


# Uso de la clase
cliente2 = ClientSocket(l[0])  
cliente3 = ClientSocket(l[1])  
cliente4 = ClientSocket(l[2])  

cliente2.start()
cliente3.start()
cliente4.start()



server.start()

'''
# Usamos la clase
server = ServerSocket('localhost')
server.start()
'''