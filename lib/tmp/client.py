import socket
import time
'''
class SocketClient:
    def __init__(self, server_ip, server_port, client_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_port = client_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', self.client_port))
        try:
            self.sock.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            print(f"No se pudo conectar al servidor en {self.server_ip}:{self.server_port}. Intentando de nuevo en 5 segundos...")
            time.sleep(5)  # Esperar 5 segundos antes de intentar de nuevo

    def send_message(self, message):
        for _ in range(5):  # Intentar reconectar 5 veces
            try:
                #self.sock.connect((self.server_ip, self.server_port))
                tiempo_inicio = time.time()
                self.sock.sendall(message.encode('utf-8'))
                data = self.sock.recv(1024)
                tiempo_fin = time.time()
                if data.decode('utf-8') == 'Estoy vivo':
                    return tiempo_fin - tiempo_inicio
                break
            except (ConnectionRefusedError, BrokenPipeError):
                print(f"No se pudo conectar al servidor en {self.server_ip}:{self.server_port}. Intentando de nuevo en 5 segundos...")
                time.sleep(5)  # Esperar 5 segundos antes de intentar de nuevo
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                break

    def close_connection(self):
        self.sock.close()
'''

class SocketClient:
    def __init__(self, server_ip, server_port, client_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_port = client_port
        self.sock = self.create_socket_and_connect()

    def create_socket_and_connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.client_port))
        for _ in range(5):  # Intentar reconectar 5 veces
            try:
                sock.connect((self.server_ip, self.server_port))
                break
            except (ConnectionRefusedError, BrokenPipeError):
                print(f"No se pudo conectar al servidor en {self.server_ip}:{self.server_port}. Intentando de nuevo en 5 segundos...")
                #time.sleep(5)  # Esperar 5 segundos antes de intentar de nuevo
            except Exception as e:
                print(f"Ocurrió un error: {e}")
        return sock

    def send_message(self, message):
        try:
            tiempo_inicio = time.time()
            self.sock.sendall(message.encode('utf-8'))
            data = self.sock.recv(1024)
            tiempo_fin = time.time()
            if data.decode('utf-8') == 'Estoy vivo':
                return tiempo_fin - tiempo_inicio
        except BrokenPipeError:
            print(f"Se perdió la conexión con el servidor en {self.server_ip}:{self.server_port}. Intentando reconectar...")
            self.sock = self.create_socket_and_connect()
            return self.send_message(message)

    def close_connection(self):
        self.sock.close()


client = SocketClient('localhost', 8080, 8090)
i = 0
while i < 100:
    tiempo = client.send_message('Como estas')
    print('Demoro {0}'.format(tiempo))
    i = i + 1
    #time.sleep(1)

