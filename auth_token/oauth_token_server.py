import os
import time

import requests

import globales


class TokenManager:
    @staticmethod
    def get_token():
        if time.time() > globales.AUTH_TOKEN_EXPIRY:
            try:
                TokenManager.refresh_token()
            except Exception as e:
                raise Exception('Error al obtener el token', e)
        return globales.AUTH_TOKEN_USUARIO

    @staticmethod
    def refresh_token():
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": globales.AUTH_REFRESH_TOKEN,
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('SECRET'),
        }
        response = requests.post(os.environ.get('TOKEN_URL'), data=data, headers=headers)
        try:
            response.raise_for_status()
            TokenManager.save_response(response)
        except requests.exceptions.HTTPError as e:
            raise Exception('Error al refrescar el token', e)

    @staticmethod
    def save_response(response):
        json_data = response.json()
        globales.AUTH_TOKEN_USUARIO = json_data["access_token"]
        globales.AUTH_REFRESH_TOKEN = json_data["refresh_token"]
        globales.AUTH_TOKEN_EXPIRY = time.time() + json_data['expires_in'] - 60

    @staticmethod
    def get_token_with_code(code, code_verifier):
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
            "code_verifier": code_verifier,
        }
        response = requests.post(os.environ.get('TOKEN_URL'), data=data, headers=headers)
        try:
            response.raise_for_status()
            TokenManager.save_response(response)
        except requests.exceptions.HTTPError as e:
            raise Exception('Error al obtener el token con codigo', e)
