import socket
import threading

class ServerSocket(threading.Thread):
    def __init__(self, ip):
        super().__init__() 
        self.ip = ip
        self.port = 8000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5) 
        self.server_socket.settimeout(1000)

    def run(self):
        print(f'Servidor corriendo en {self.ip}:{self.port}')
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f'Conexión entrante aceptada desde {addr}')
            data = client_socket.recv(1024)
            print(f'Datos recibidos: {data.decode()}')
            response = 'Mensaje recibido'
            client_socket.send(response.encode())
            client_socket.close()


class ClientSocket(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = 8000

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(b'Hola, servidor')
            data = s.recv(1024)
        print('Recibido', repr(data))




# Uso de la clase
#cliente = ClientSocket('localhost')  # Utiliza un puerto diferente al del servidor
#cliente.start()


'''
# Usamos la clase
server = ServerSocket('localhost')
server.start()
'''