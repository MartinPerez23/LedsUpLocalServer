import os
import sys


def resource_path(relative_path):
    if getattr(sys, 'nuitka_onefile_compression', False):
        base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


REPETICION = True
AUTH_TOKEN_USUARIO = None
AUTH_TOKEN_EXPIRY = None
AUTH_REFRESH_TOKEN = None
