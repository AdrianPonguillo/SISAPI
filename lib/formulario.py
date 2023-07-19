from lib.db import Data
import uuid
import json

class Formulario():
    """
    Generacion de datos almacenados en un diccionario para ser llevados a RabbitMQ y posteriormente a un archivo.

    Métodos:
        __init__(): Inicializador de objetos
        crear_formulario(): Genera el diccionario llamando a funciones que devuelven datos aleatorios de una base de datos
        formulario_to_json(): Convierte el diccionario a json
    """

    def __init__(self):
        self.identificador = str(uuid.uuid4())
        self.data = Data()
        self.crear_formulario()

    def crear_formulario(self):
        genero = self.data.get_genero()
        self.informacion_persona = {
            self.identificador: {
                "informacion_personal": {
                    "user_id": self.data.get_identificador_pasaporte(),
                    "genero": genero,
                    "nombres": self.data.get_nombres(genero),
                    "apellidos": self.data.get_apellidos(),
                    "lugar_nacimiento": self.data.get_lugarnacimiento(),
                    "estado_civil": self.data.get_estado_civil(),
                    "edad": self.data.get_edad(),
                    "religion": self.data.get_religion(),
                    "postura_politica": self.data.get_postura_politica(),
                },
                "informacion_demografica": {
                    "profesiones": self.data.get_profesiones(),
                    "edad": self.data.get_edad(),
                    "lugar_nacimiento": self.data.get_lugarnacimiento(),
                },
                "gustos": {
                    "hobbies": self.data.get_hobbies(),
                    "colores_favoritos": self.data.get_colores(),
                    "equipo_futbol": self.data.get_equipo_futbol(),
                    "mascotas": self.data.get_mascotas(),
                    "modelos_autos": self.data.get_modelos_autos(),
                    "paise_conocidos": self.data.get_paises(),
                },
                "salud": {
                    "enfermedades_raras": self.data.get_enfermedades_raras(),
                    "alergias": self.data.get_alergias(),
                    "deportes_practicados": self.data.get_deportes(),
                },
                "habilidades": {
                    "habilidades_tecnicas": self.data.get_habilidades_tecnicas(),
                    "habilidades_personales": self.data.get_habilidades_personales(),
                    "habilidades_varias": self.data.get_habilidades_varias(),
                }
            }
        }
        
    def formulario_to_json(self):
        return json.dumps(self.informacion_persona)
