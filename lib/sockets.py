import socket
import time
import configparser
import threading

# Leer el archivo de configuración
config = configparser.ConfigParser()
config.read('config.ini')

# Obtener la lista de nodos
nodos = [s for s in config.sections() if s != 'olimpo']

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# usamos el DNS de Google para obtener la dirección IP local
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()


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
                    if data.decode('utf-8') == 'Como estas':
                        conn.sendall(b'Estoy vivo')


class SocketClient:
    def __init__(self, server_ip, server_port, client_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_port = client_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', self.client_port))
        self.sock.connect((self.server_ip, self.server_port))

    def send_message(self, message):
        try:
            tiempo_inicio = time.time()
            self.sock.sendall(message.encode('utf-8'))
            data = self.sock.recv(1024)
            tiempo_fin = time.time()
            if data.decode('utf-8') == 'Estoy vivo':
                return tiempo_fin - tiempo_inicio
        except Exception as e:
            print(f"No se pudo enviar el mensaje al servidor en {self.server_ip}:{self.server_port}, error: {e}")
            
    def close_connection(self):
        self.sock.close()



# Lanzar los servidores
for nodo in nodos:
    nodo_ip = config[nodo]['ip']
    if nodo_ip != local_ip:
        server = SocketServer(nodo_ip, int(config[nodo]['puertos_entrada']))
        threading.Thread(target=server.start_server).start()

# Realizar las comunicaciones
resultados = {}
for nodo1 in nodos:
    for nodo2 in nodos:
        nodo1_ip = config[nodo1]['ip']
        nodo2_ip = config[nodo2]['ip']
        if nodo1_ip != local_ip and nodo2_ip != local_ip:  # solo se conecta si ninguno de los nodos es el local
            client = SocketClient(nodo2_ip, int(config[nodo2]['puertos_entrada']), int(config[nodo1]['puertos_salida']))
            tiempo = client.send_message('Como estas')
            resultados[(nodo1, nodo2)] = tiempo
            client.close_connection()

# Imprimir los resultados
for nodo, tiempo in resultados.items():
    print(f'De {nodo[0]} a {nodo[1]}: {tiempo} segundos')
