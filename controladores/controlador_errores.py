import os
import traceback

import requests

from auth_token.oauth_token_server import TokenManager
from vistas.vista_popup_mensaje import PopupMensaje


class ControladorErrores:
    def __init__(self, vista):
        """
        Inicializa el controlador con la vista que notificará al usuario.

        :param vista: La vista asociada para mostrar mensajes.
        """
        self.vista = vista

    def enviar_error(self, modelo_error):
        """
        Envía un reporte de error basado en un objeto ModeloError.

        :param modelo_error: Instancia de ModeloError con los detalles del error.
        """
        try:
            token = TokenManager.get_token()
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            response = requests.post(
                os.environ.get('ERROR_URL'),
                json=modelo_error.to_dict(),
                headers=headers
            )

            if response.status_code != 201:
                raise Exception('Error al enviar reporte')

            PopupMensaje(self.vista, 'Error reportado, espera a ser contactado por el equipo de soporte', False)

        except Exception as e:
            print("Error al enviar el reporte: ", e)
            traceback.print_exc()
            PopupMensaje(self.vista, 'No se ha podido enviar el error, por favor contacte vía web', True)
