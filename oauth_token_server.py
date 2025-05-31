import requests
import os
from dotenv import load_dotenv


load_dotenv()

class OAuthTokenServer:
    def __init__(self, code_verifier):
        self.client_id = os.environ.get('CLIENT_ID')
        self.token_url = os.environ.get('TOKEN_URL')
        self.redirect_uri = os.environ.get('REDIRECT_URL')
        self.code_verifier = code_verifier
        self.access_token = None
        self.refresh_token = None
        self.expiry = None


    def do_post(self,code):
        TOKEN_URL = "http://TU_SERVIDOR/o/token/"

        data = {
            "grant_type": "authorization_code",
            "code": "EL_AUTHORIZATION_CODE",
            "redirect_uri": "http://localhost:34123/callback",
            "client_id": "TU_CLIENT_ID",
            "code_verifier": "EL_CODE_VERIFIER",  # solo si usás PKCE
        }

        response = requests.post(TOKEN_URL, data=data)