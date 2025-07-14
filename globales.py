import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, ya sea en desarrollo o ejecutable."""
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)


REPETICION = True
AUTH_TOKEN_USUARIO = None
AUTH_TOKEN_EXPIRY = None
AUTH_REFRESH_TOKEN = None
