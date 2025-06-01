import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class OAuthTokenServer:
    def __init__(self, code_verifier):
        self.code_verifier = code_verifier

    def get_token(self, code):
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.environ.get('REDIRECT_URL'),
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('SECRET'),
            "code_verifier": self.code_verifier,
        }

        print("======== DATOS QUE SE ENVIARÁN ========")
        print("TOKEN_URL:", os.environ.get('TOKEN_URL'))
        print("client_id:", data["client_id"])
        print("client_secret:", data["client_secret"])
        print("redirect_uri:", data["redirect_uri"])
        print("grant_type:", data["grant_type"])
        print("code:", data["code"])
        print("code_verifier:", data["code_verifier"])
        print("headers:", headers)
        print("=======================================")

        try:
            response = requests.post(os.environ.get('TOKEN_URL'), data=data, headers=headers, verify=False)
            response.raise_for_status()  # Lanza el error si el status code es 4xx/5xx
        except requests.exceptions.HTTPError as e:
            print("Status code:", response.status_code)
            print("Respuesta del servidor:")
            print(response.text)  # <-- Acá ves el JSON o mensaje de error
            raise

        print(response.json())