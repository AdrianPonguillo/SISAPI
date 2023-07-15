import socket
import threading
#import configparser


# Leer el archivo de configuración
#config = configparser.ConfigParser()
#config.read('config.ini')

# Obtener la lista de nodos
#nodos = [s for s in config.sections() if s != 'olimpo']


class SocketServer:
    def __init__(self, host = '0.0.0.0', port = 8000):
        self.host = host
        self.port = port

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Servidor iniciado en {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    print(data)
                    if data.decode('utf-8') == 'Como estas':
                        conn.sendall(b'Estoy vivo')
                        




server = SocketServer('localhost', 8080)
threading.Thread(target=server.start_server).start()