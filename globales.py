import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


REPETICION = True
AUTH_TOKEN_USUARIO = None
AUTH_TOKEN_EXPIRY = None
AUTH_REFRESH_TOKEN = None
