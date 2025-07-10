import os
import sys

def resource_path(relative_path):
    if hasattr(sys, 'frozen') or getattr(sys, 'nuitka_compiled', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)
    print(f"DEBUG resource_path: {full_path}")
    return full_path


REPETICION = True
AUTH_TOKEN_USUARIO = None
AUTH_TOKEN_EXPIRY = None
AUTH_REFRESH_TOKEN = None
