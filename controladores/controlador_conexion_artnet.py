import random
import threading
import time

import globales


class ConexionArtnet:
    def __init__(self, gestor_dispositivos):
        self.gestor = gestor_dispositivos
        self.coloresScroll = [
            "#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00", "#00FF80",
            "#00FFFF", "#0080FF", "#0000FF", "#8000FF", "#FF00FF", "#FF0080",
        ]

    def efecto_probar(self):
        for dispositivo in self.gestor.obtener_dispositivos():
            dispositivo.datosAEnviar = [255] * 512
            dispositivo.enviar_datos()
            time.sleep(1)
            dispositivo.datosAEnviar = [0] * 512
            dispositivo.enviar_datos()

    def efecto_color(self, data_json):
        color = data_json['color']
        velocidad = int(data_json['velocidad'])
        cambio_constante = data_json['cambio_constante'] == 'checked'

        if cambio_constante:
            actual = 0
            while globales.REPETICION:
                color = self.coloresScroll[actual % len(self.coloresScroll)]
                self.enviar_color(color)
                actual += 1
                time.sleep(3 / velocidad)
        else:
            self.enviar_color(color)

    def enviar_color(self, color):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        for d in self.gestor.obtener_dispositivos():
            d.datosAEnviar = [r, g, b] * (d.matrizX * d.matrizY)
            d.enviar_datos()

    def efecto_scroll(self, data_json):
        velocidad = int(data_json['velocidad'])
        direccion = data_json['direccion']

        while globales.REPETICION:
            for d in self.gestor.obtener_dispositivos():
                d.datosAEnviar.clear()
                for y in range(d.matrizY):
                    for x in range(d.matrizX):
                        if direccion == 'Izquierda':
                            i = (x + d.contador) % len(self.coloresScroll)
                        elif direccion == 'Derecha':
                            i = (x - d.contador) % len(self.coloresScroll)
                        elif direccion == 'Arriba':
                            i = (y + d.contador) % len(self.coloresScroll)
                        elif direccion == 'Abajo':
                            i = (y - d.contador) % len(self.coloresScroll)
                        else:
                            i = (x + d.contador) % len(self.coloresScroll)

                        c = self.coloresScroll[i]
                        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
                        d.datosAEnviar.extend([r, g, b])

                d.contador = (d.contador + 1) % len(self.coloresScroll)
                threading.Thread(target=d.enviar_datos, daemon=True).start()
            time.sleep(1 / velocidad)

    def efecto_scan(self, data_json):
        velocidad = int(data_json['velocidad'])
        direccion = data_json['direccion']
        color_scan = data_json['colorScan']
        color_fondo = data_json['colorFondo']

        r_s, g_s, b_s = int(color_scan[1:3], 16), int(color_scan[3:5], 16), int(color_scan[5:7], 16)
        r_f, g_f, b_f = int(color_fondo[1:3], 16), int(color_fondo[3:5], 16), int(color_fondo[5:7], 16)

        while globales.REPETICION:
            for d in self.gestor.obtener_dispositivos():
                d.datosAEnviar = [r_f, g_f, b_f] * (d.matrizX * d.matrizY)
                if direccion == 'Derecha':
                    pos = d.contador % d.matrizX
                    for y in range(d.matrizY):
                        idx = y * d.matrizX + pos
                        d.datosAEnviar[idx * 3:idx * 3 + 3] = [r_s, g_s, b_s]
                elif direccion == 'Izquierda':
                    pos = d.matrizX - (d.contador % d.matrizX) - 1
                    for y in range(d.matrizY):
                        idx = y * d.matrizX + pos
                        d.datosAEnviar[idx * 3:idx * 3 + 3] = [r_s, g_s, b_s]
                elif direccion == 'Abajo':
                    pos = d.contador % d.matrizY
                    for x in range(d.matrizX):
                        idx = pos * d.matrizX + x
                        d.datosAEnviar[idx * 3:idx * 3 + 3] = [r_s, g_s, b_s]
                elif direccion == 'Arriba':
                    pos = d.matrizY - (d.contador % d.matrizY) - 1
                    for x in range(d.matrizX):
                        idx = pos * d.matrizX + x
                        d.datosAEnviar[idx * 3:idx * 3 + 3] = [r_s, g_s, b_s]

                d.contador = (d.contador + 1) % (d.matrizX if direccion in ['Derecha', 'Izquierda'] else d.matrizY)
                threading.Thread(target=d.enviar_datos, daemon=True).start()
            time.sleep(1 / velocidad)

    def efecto_estrellas(self, data_json):
        velocidad = int(data_json['velocidad'])
        color_estrellas = data_json['colorEstrellas']
        color_fondo = data_json['colorFondo']

        r_s, g_s, b_s = int(color_estrellas[1:3], 16), int(color_estrellas[3:5], 16), int(color_estrellas[5:7], 16)
        r_f, g_f, b_f = int(color_fondo[1:3], 16), int(color_fondo[3:5], 16), int(color_fondo[5:7], 16)

        while globales.REPETICION:
            for d in self.gestor.obtener_dispositivos():
                d.datosAEnviar = [r_f, g_f, b_f] * (d.matrizX * d.matrizY)
                for _ in range(d.matrizX * d.matrizY // 3):
                    idx = random.randint(0, d.matrizX * d.matrizY - 1)
                    d.datosAEnviar[idx * 3:idx * 3 + 3] = [r_s, g_s, b_s]
                threading.Thread(target=d.enviar_datos, daemon=True).start()
            time.sleep(3 / velocidad)
