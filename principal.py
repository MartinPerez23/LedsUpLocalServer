import globales
import vistas.vista_login as login
import vistas.vista_principal as app_view


if __name__ == "__main__":
    app = login.Login()
    app.mainloop()

    if globales.AUTH_TOKEN_USUARIO is not None:
        app = app_view.AppView()
        app.mainloop()
