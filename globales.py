import os
import sys


def resource_path(relative_path):
    frozen = getattr(sys, 'frozen', False)
    meipass = getattr(sys, '_MEIPASS', None)

    print(f"DEBUG resource_path: frozen={frozen}, _MEIPASS={meipass}")

    if frozen and meipass:
        base_path = meipass
    else:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)
    print(f"DEBUG resource_path: full_path={full_path}")
    return full_path


REPETICION = True
AUTH_TOKEN_USUARIO = None
AUTH_TOKEN_EXPIRY = None
AUTH_REFRESH_TOKEN = None
