import requests 
from urllib.parse import unquote
import json
import re
#Consumidor temporal de servicios api
def fetch_and_print_file():
    response = requests.get('http://localhost:8080/get_file')

    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = re.findall('filename=(.+)', content_disposition)[0]
    else:
        filename = 'default.json' 

    with open(filename, 'wb') as f:
        f.write(response.content)
    
    with open(filename, 'r') as f:
        content = json.load(f)

    content_str = json.dumps(content , ensure_ascii=False)
    print(content_str)
    

fetch_and_print_file()