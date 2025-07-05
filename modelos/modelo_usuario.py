import os

import requests


class ModeloUsuario:
    def __init__(self, access_token):
        self.access_token = access_token

    def obtener_nombre_usuario(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        try:
            response = requests.get(os.environ.get("USER_INFO_URL"), headers=headers)
            if response.status_code != 200:
                raise Exception('Error al obtener información del usuario')

            data = response.json()
            return data.get('user_name')

        except requests.RequestException as e:
            raise Exception('Error de red', e)
