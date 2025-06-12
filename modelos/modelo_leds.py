class ModeloLEDs:
    def __init__(self):
        self.estado_leds = {}  # {id_dispositivo: accion}

    def clear_estado_leds(self):
        self.estado_leds = {}

    def add_estado_leds(self, nombre_dispositivo, accion):
        self.estado_leds[nombre_dispositivo] = accion

    def get_estado_leds(self):
        return self.estado_leds
