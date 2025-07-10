from dotenv import load_dotenv

import globales
import vistas.vista_login as login
import vistas.vista_principal as app_view

if __name__ == "__main__":

    import sys

    print(f"DEBUG: sys.frozen? {hasattr(sys, 'frozen')}")
    print(f"DEBUG: nuitka_compiled? {getattr(sys, 'nuitka_compiled', False)}")
    print(f"DEBUG: sys.executable = {sys.executable}")
    print(f"DEBUG: __file__ = {__file__}")

    load_dotenv(dotenv_path=globales.resource_path('.env'))

    app = login.Login()
    app.mainloop()

    if globales.AUTH_TOKEN_USUARIO is not None:
        app = app_view.AppView()
        app.mainloop()
