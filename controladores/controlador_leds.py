# controladores/controlador_leds.py
import threading
import time

import globales
from modelos.modelo_leds import ModeloLEDs
from controladores.gestordispositivos import GestorDispositivos
from controladores.conexion_artnet import ConexionArtnet


def detener_theads_viejos():
    globales.REPETICION = False
    time.sleep(2)
    globales.REPETICION = True


class ControladorLEDs:
    def __init__(self):
        self.modelo = ModeloLEDs()
        self.gestor = GestorDispositivos()
        self.conexion = ConexionArtnet(self.gestor)

    def procesar_comando(self, data_json, app_view):
        detener_theads_viejos()

        lista_dispositivos = self._formatear_lista(data_json['lista'])
        self.gestor.actualizar_lista(lista_dispositivos)

        self.modelo.clear_estado_leds()
        for d in lista_dispositivos:
            self.modelo.add_estado_leds(d['nombre'], data_json['accion'])

        app_view.dispositivosFrame.actualizar_dispositivos(self.modelo.get_estado_leds())

        accion = data_json['accion']
        if accion == 'probar':
            self.conexion.efecto_probar()
        elif accion == 'color':
            threading.Thread(target=self.conexion.efecto_color, args=(data_json,), daemon=True).start()
        elif accion == 'scroll':
            threading.Thread(target=self.conexion.efecto_scroll, args=(data_json,), daemon=True).start()
        elif accion == 'scan':
            threading.Thread(target=self.conexion.efecto_scan, args=(data_json,), daemon=True).start()
        elif accion == 'estrellas':
            threading.Thread(target=self.conexion.efecto_estrellas, args=(data_json,), daemon=True).start()

    def _formatear_lista(self, lista_json):
        lista = []
        for i in range(0, len(lista_json), 8):
            orden_map = {
                'Arriba-Izquierda': 0, 'Arriba': 1, 'Arriba-Derecha': 2,
                'Izquierda': 3, 'Centro': 4, 'Derecha': 5,
                'Abajo-Izquierda': 6, 'Abajo': 7, 'Abajo-Derecha': 8
            }
            lista.append({
                'ip': lista_json[i],
                'universo': int(lista_json[i+1]),
                'matriz_x': int(lista_json[i+2]),
                'matriz_y': int(lista_json[i+3]),
                'patch': lista_json[i+4],
                'orden': orden_map.get(lista_json[i+5], 4),
                'tipo_led': lista_json[i+6],
                'nombre': lista_json[i+7],
            })
        return lista
