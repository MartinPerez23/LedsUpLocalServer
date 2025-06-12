import os

import requests


class ModeloError:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def enviar_error(self, detalle, contexto):
        if not self.auth_token:
            raise Exception('No hay token de autenticación')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }

        error_data = {
            'detalle': detalle,
            'contexto': contexto,
            'origen': 'app'
        }

        response = requests.post(
            os.environ.get('ERROR_URL'),
            json=error_data,
            headers=headers,
            verify=False
        )

        if response.status_code != 201:
            raise Exception('Error al enviar reporte')

        return response.status_code
