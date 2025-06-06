
import os
import time
import requests
from dotenv import load_dotenv

import globales

load_dotenv()


class OAuthTokenServer:

    def __init__(self, code_verifier):
        self.code_verifier = code_verifier
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0

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

        try:
            response = requests.post(os.environ.get('TOKEN_URL'), data=data, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return

        self.save_response(response)


    def get_access_token(self):
        now = time.time()
        if self.access_token is None or now > self.token_expiry:
            self.refresh_access_token()
        return self.access_token

    def refresh_access_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('SECRET'),
        }
        response = requests.post(os.environ.get('TOKEN_URL'), data=data, headers=headers, verify=False)
        self.save_response(response)

    def save_response(self, response):
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]
        self.token_expiry = time.time() + response.json()['expires_in'] - 60
        globales.TOKEN_USER = self.access_token
