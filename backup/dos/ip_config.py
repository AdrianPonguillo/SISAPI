import socket

class Ip:

    nodos = [
        {'name': 'dist4', 'ip':'172.27.176.5', 'port-a': 8000, 'port-b': 9000},
        {'name': 'dist5', 'ip':'172.27.176.6', 'port-a': 8000, 'port-b': 9000},
        {'name': 'dist6', 'ip':'172.27.176.7', 'port-a': 8000, 'port-b': 9000},
        {'name': 'dist7', 'ip':'172.27.176.8', 'port-a': 8000, 'port-b': 9000},
    ]

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        #return '172.27.176.8'
        return local_ip
    
    def get_other_ips(self):
        other = []
        for i in self.nodos:
            if i['ip'] != self.get_local_ip():
                other.append(i)
        return other
    

l = Ip().get_other_ips()
print(l)