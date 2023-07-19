import pika

class Conexion():
    """
    Clase de administración de RabbitMQ del proyecto, controla la conexion como el envio y consumo de los datos de la cola
    
    Atributos:
        user: Usuario del servidor de RabbitMQ
        password: Contraseña del servicio
        server: IP del servidor
        port: Puerto de escucha de la cola 
        virtual_host: Host de rabbitMQ
        queue: Cola del proyecto
        
    Métodos:
        __init__(): Inicializacion de la clase, parametros del modulo
        def_send(message): Envia a la cola el message
        def consuming(callback): Captura cada mensaje que entra en la cola, controlando que sea entregado
    """
    user = "pythoners"
    password = "Pythoners123"
    server = "20.121.117.150"
    port = 5672
    virtual_host = "/"
    queue = 'Forms_queue'
    
    def __init__(self):
        credential = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.server, self.port, virtual_host=self.virtual_host ,credentials = credential)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)        

    def send(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)

    def consuming(self, callback):
        self.channel.basic_consume(queue= self.queue , on_message_callback=callback, auto_ack=False)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

