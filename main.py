from lib.zoo import Node

def main():
    node = Node()  # Crear una instancia de Node
    node.connect()  # Conectar la instancia a ZooKeeper
    node.run_for_leadership()  # Comenzar a intentar convertirse en líder

if __name__ == "__main__":
    main()

























'''
def main():
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    nodes_info = [
        {'name': 'dist4', 'ip': '172.27.176.5', 'port': 8000},
        {'name': 'dist5', 'ip': '172.27.176.6', 'port': 8000},
        {'name': 'dist6', 'ip': '172.27.176.7', 'port': 8000},
        {'name': 'dist7', 'ip': '172.27.176.8', 'port': 8000},
        #{'name': 'dist8', 'ip': '172.28.252.102', 'port': 8000},
    ]

    def get_hostname(ip):
        for node in nodes_info:
            if node['ip'] == ip:
                print(node)
                return node
        return None 
    
    def get_nodes_valids():
        nodes = []
        for nodo in nodes_info:
            if nodo['ip'] != get_local_ip():
                nodes.append(nodo)
        return nodes

    local_ip = get_local_ip()
    #print(local_ip)
    nodes_valids = get_nodes_valids()
    current_node_info = get_hostname(local_ip)
    node_name = current_node_info['name']
    node_port = current_node_info['port']

    node = Node(node_name, local_ip, node_port, nodes_valids)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(node.start())
    loop.run_forever()

if __name__ == "__main__":
    os.system('clear')
    main()

'''


