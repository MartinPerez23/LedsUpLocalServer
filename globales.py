import os
import sys


def resource_path(relative_path):
    """ Obtiene la ruta absoluta a un recurso, funciona para desarrollo y para el ejecutable de Nuitka. """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


REPETICION = True
AUTH_TOKEN_USUARIO = None
AUTH_TOKEN_EXPIRY = None
AUTH_REFRESH_TOKEN = None
