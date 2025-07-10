import sys

from dotenv import load_dotenv

import globales
import vistas.vista_login as login
import vistas.vista_principal as app_view

if __name__ == "__main__":
    print("nuitka_onefile_compression?", getattr(sys, "nuitka_onefile_compression", False))
    print("nuitka_compiled?", getattr(sys, "nuitka_compiled", False))
    print("executable:", sys.executable)
    print("__file__:", __file__)

    for attr in dir(sys):
        if "nuitka" in attr.lower():
            print(f"{attr} = {getattr(sys, attr)}")

    load_dotenv(dotenv_path=globales.resource_path('.env'))

    app = login.Login()
    app.mainloop()

    if globales.AUTH_TOKEN_USUARIO is not None:
        app = app_view.AppView()
        app.mainloop()
