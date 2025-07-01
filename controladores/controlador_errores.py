import globales
from modelos.modelo_error import ModeloError
from vistas.vista_popup_mensaje import PopupMensaje


def enviar_error_a_la_web(detalle, contexto, vista):
    try:
        if globales.AUTH_TOKEN_USUARIO is None:
            PopupMensaje(vista,
                         'No se puede enviar el error, no hay usuario autenticado. Intente ingregar nuevamente',
                         True)
            return

        ModeloError.enviar_error(detalle, contexto)
        PopupMensaje(vista,
                     'Error reportado, espera a ser contactado por el equipo de soporte',
                     False)

    except Exception as e:
        PopupMensaje(vista,
                     'No se ha podido enviar el error, por favor contacte via web',
                     True)
