import lib.webclient
import lib.webserver
import lib.ip_config as ip
import socket



print(ip.nodos)

hostname = socket.gethostname()

# Obtener la dirección IP local
ip_address = socket.gethostbyname(hostname)

print("El nombre del host es: " + hostname)
print("La dirección IP local es: " + ip_address)


ip_address = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)[0][4][0]

print("La dirección IP local es: " + ip_address)