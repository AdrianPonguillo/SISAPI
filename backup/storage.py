from lib.config import Config
from lib.node import Node 
import socket
import time

config = Config('config.ini')
nodes_info = config.get_all_nodes()

#print(nodes_info)
print('*'*40)

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

self_ip = get_private_ip() 
#self_ip = '10.2.0.9:8000'
#self_ip = '10.2.0.9'
#print(self_ip)

nodes = []

ips = [str(info['ip']) + ':' + str(info['puertos_entrada']) for name, info in nodes_info.items() if str(info['ip'])  != self_ip]
ip_local = [str(info['ip']) + ':' + str(info['puertos_entrada']) for name, info in nodes_info.items() if str(info['ip']) == self_ip]
if ip_local is None:
    ip_local = self_ip
else:
    ip_local = ip_local[0]

print(ips)
print(ip_local)
node = Node(ip_local, ips) 

'''
for node_name, node_info in nodes_info.items():
    ips = [str(info['ip']) + ':' + str(info['puertos_entrada']) for name, info in nodes_info.items() if str(info['ip'])  != self_ip]
    ip_local = [str(info['ip']) + ':' + str(info['puertos_entrada']) for name, info in nodes_info.items() if str(info['ip']) == self_ip]
    if ip_local is None:
        ip_local = self_ip
    else:
        ip_local = ip_local[0]
    #print(node_name)
    #print(node_info)
    #self_ip = node_info['ip']
    #partner_ips = [info['ip'] for name, info in nodes_info.items() if name != node_name]
    #print(self_ip)
    print(ips)
    print(ip_local)
    node = Node(ip_local, ips)
    nodes.append(node)
'''


# Realiza operaciones con los nodos...
#for node in nodes:
while True:
    node.tick()
    print(node.is_alive())
    print(node.is_leader())
    print(node.get_partners())
    time.sleep(20)

