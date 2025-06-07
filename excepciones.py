import os
import requests

def post_error(detalle, contexto,token):

    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {token.strip()}'
    }

    data = {
        "detalle" : detalle,
        "contexto": contexto,
        "origen": "app"
    }

    print("TOKEN:", repr(token))
    print("HEADERS:", headers)

    response = requests.post(os.environ.get('ERROR_URL'), json=data, headers=headers, verify=False)

    response.json()