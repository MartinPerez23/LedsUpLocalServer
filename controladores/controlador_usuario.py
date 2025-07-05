import traceback

import globales
from modelos.modelo_usuario import ModeloUsuario
from vistas.vista_popup_mensaje import PopupMensaje


class ControladorUsuario:
    def __init__(self):
        self.modelo_usuario = ModeloUsuario(globales.AUTH_TOKEN_USUARIO)
        self.user_name = None

        self.set_user_name()

    def set_user_name(self):
        try:
            self.user_name = self.modelo_usuario.obtener_nombre_usuario()
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

            PopupMensaje(None, 'Error reportado, espera a ser contactado por el equipo de soporte', True)

    def get_user_name(self):
        return self.user_name
