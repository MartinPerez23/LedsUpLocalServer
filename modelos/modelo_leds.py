class ModeloLEDs:
    def __init__(self):
        self.estado_leds = {}  # {id_dispositivo: accion}

    def actualizar_estado_led(self, nombre_dispositivo, accion):
        self.estado_leds[nombre_dispositivo] = accion

    def obtener_estado_led(self):
        return self.estado_leds
