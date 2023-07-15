import socket

class SocketServer:
    def __init__(self, host = '0.0.0.0', port = 8000):
        self.host = host
        self.port = port

    def start_server(self):
        # Crear un socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Enlazar el socket a la dirección y puerto
            s.bind((self.host, self.port))

            # Escuchar conexiones entrantes
            s.listen()

            print(f"Servidor escuchando en {self.host}:{self.port}...")

            while True:
                # Aceptar una conexión entrante
                conn, addr = s.accept()
                with conn:
                    print(f"Conexión entrante desde {addr}")

                    # Recibir datos
                    data = conn.recv(1024)

                    # Si los datos recibidos son 'Como estas', entonces responder 'Estoy vivo'
                    if data.decode('utf-8') == 'Como estas':
                        conn.sendall(b'Estoy vivo')
                    else:
                        conn.sendall(b'Mensaje no reconocido')
