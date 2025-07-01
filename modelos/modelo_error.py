import os

import requests

from auth_token.oauth_token_server import TokenManager


class ModeloError:

    def enviar_error(self, detalle, contexto):
        token = TokenManager.get_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
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
        )

        if response.status_code != 201:
            raise Exception('Error al enviar reporte')

        return response.status_code
