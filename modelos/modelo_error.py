class ModeloError:
    def __init__(self, detalle, contexto, origen="app"):
        """
        Inicializa un nuevo objeto ModeloError con los detalles del error.

        :param detalle: Descripción del error.
        :param contexto: Contexto adicional relacionado con el error.
        :param origen: Origen del error (por defecto, 'app').
        """
        self.detalle = detalle
        self.contexto = contexto
        self.origen = origen

    def to_dict(self):
        """
        Convierte el modelo de error a un diccionario para facilitar su envío.

        :return: Diccionario con los datos del error.
        """
        return {
            'detalle': self.detalle,
            'contexto': self.contexto,
            'origen': self.origen
        }
