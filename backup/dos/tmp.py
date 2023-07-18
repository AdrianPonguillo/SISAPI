import json
import requests
from repository import Repository
'''
enviar = {}
with open('./files/COL0000272.json', 'r', encoding='iso-8859-1') as f:
    dato = json.loads(f.read())
    #print(dato)
    first_key = next(iter(dato))
    iper = dato[first_key]
    enviar['record'] = iper
    #print(iper)
    #print(iper['informacion_personal']['user_id'])
    print(enviar)
'''

endpoint='http://20.55.70.215:8080/get_file'

def get_data():
        try:
            response = requests.get(endpoint)
            data = response.json()
            return data
        except Exception as ex:
            print('Se ha producido un error:' + str(ex))
            return False
        
a = get_data()

for key, value in a.items():
    user_id = value['informacion_personal']['user_id']
    print(f"El user_id es: {user_id}")

print(a)

partitions = {}

repos = Repository()
#repos.regenerate_index(partitions)
partitions = repos.get_index()
#print(partitions)


repos.set_data(a)
r = repos.save_data(partitions)



Repository().save_index(partitions)    
#clave9878
#clave9193

print(repos.read_data('MEX9156637', partitions))
#print(repos.read_data('clave190', partitions))
#print(repos.read_data('clave115', partitions))
#print(partitions)'''