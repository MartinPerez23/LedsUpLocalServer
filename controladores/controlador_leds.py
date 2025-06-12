import threading
import time

from conexiones import conexion_artnet
import globales
from modelos.modelo_leds import ModeloLEDs


def detener_theads_viejos():
    globales.REPETICION = False
    time.sleep(2)
    globales.REPETICION = True


class ControladorLEDs:
    def __init__(self):
        self.artnet = conexion_artnet.ConexionArtnet()
        self.modelo = ModeloLEDs()

    def procesar_comando(self, data_json, app_view):
        self.artnet.dispositivosActivos.clear()
        accion = data_json['accion']
        dispositivos_actuales = data_json['lista']
        numero_dispositivos = int(len(dispositivos_actuales) / 7)

        for repeticion in range(numero_dispositivos):
            numero = repeticion * 8
            ip = dispositivos_actuales[numero]
            universo = int(dispositivos_actuales[numero + 1])
            matriz_x = int(dispositivos_actuales[numero + 2])
            matriz_y = int(dispositivos_actuales[numero + 3])
            patch = dispositivos_actuales[numero + 4]
            orden = dispositivos_actuales[numero + 5]
            tipo_led = dispositivos_actuales[numero + 6]
            nombre_dispositivo = dispositivos_actuales[numero + 7]

            orden_map = {
                'Arriba-Izquierda': 0, 'Arriba': 1, 'Arriba-Derecha': 2,
                'Izquierda': 3, 'Centro': 4, 'Derecha': 5,
                'Abajo-Izquierda': 6, 'Abajo': 7, 'Abajo-Derecha': 8
            }
            orden = orden_map.get(orden, 4)

            self.artnet.buscar_o_agregar_dispositivo(ip, universo, patch, matriz_x, matriz_y, orden, tipo_led)
            self.modelo.actualizar_estado_led(nombre_dispositivo, accion)
            app_view.dispositivosFrame.actualizar_dispositivos(self.modelo.obtener_estado_led())

        self.artnet.dispositivosActivos = sorted(
            self.artnet.dispositivosActivos, key=lambda d: d.orden
        )

        self.artnet.print_cantidad_dispositivos_activos()
        self.artnet.print_dispositivos_activos()

        if accion == 'probar':
            detener_theads_viejos()
            self.artnet.probar_dispositivo()

        elif accion == 'color':
            detener_theads_viejos()
            t = threading.Thread(target=self.artnet.color, args=(data_json,), daemon=True)
            t.start()

        elif accion == 'scroll':
            detener_theads_viejos()
            t = threading.Thread(target=self.artnet.scroll, args=(data_json,), daemon=True)
            t.start()

        elif accion == 'scan':
            detener_theads_viejos()
            t = threading.Thread(target=self.artnet.scan, args=(data_json,), daemon=True)
            t.start()

        elif accion == 'estrellas':
            detener_theads_viejos()
            t = threading.Thread(target=self.artnet.estrellas, args=(data_json,), daemon=True)
            t.start()
