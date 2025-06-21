import globales
from vistas.vista_popup_mensaje import PopupMensaje
from auth_token.oauth_token_server import TokenManager
import requests
import os

def enviar_error_a_la_web(self, detalle, contexto, vista):
    try:
        if not globales.AUTH_TOKEN_USUARIO:
            PopupMensaje(vista,
                        'No se puede enviar el error, no hay usuario autenticado. Intente ingregar nuevamente',
                            True)
            return

        enviar_error(detalle, contexto)
        PopupMensaje(vista,
                         'Error reportado, espera a ser contactado por el equipo de soporte',
                         False)

    except Exception as e:
        PopupMensaje(vista,
                'No se ha podido enviar el error, por favor contacte via web',
                    True)


def enviar_error(detalle, contexto):

    token = TokenManager.get_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    error_data = {
        'detalle': detalle,
        'contexto': contexto,
        'origen': 'app'
    }

    response = requests.post(
        os.environ.get('ERROR_URL'),
        json=error_data,
        headers=headers,
        verify=False
    )

    if response.status_code != 201:
        raise Exception('Error al enviar reporte')

    return response.status_code
