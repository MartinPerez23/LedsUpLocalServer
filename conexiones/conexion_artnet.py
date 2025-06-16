import random
import threading
import time

import conexiones.dispositivo_artnet as dispositivo_artnet
import globales


class ConexionArtnet:
    def __init__(self):
        self.matrizX0 = 0
        self.matrizX1 = 0
        self.matrizX2 = 0

        self.matrizY0 = 0
        self.matrizY1 = 0
        self.matrizY2 = 0

        self.dispositivosActivos = list()
        self.coloresScroll = [
            "#FF0000",
            "#FF8000",
            "#FFFF00",
            "#80FF00",
            "#00FF00",
            "#00FF80",
            "#00FFFF",
            "#0080FF",
            "#0000FF",
            "#8000FF",
            "#FF00FF",
            "#FF0080",
        ]

    def actualizar_maximo_matriz_x_matriz_y(self, dispositivo):
        if dispositivo.orden == 0:
            if self.matrizY0 < dispositivo.matrizY:
                self.matrizY0 = dispositivo.matrizY
            if self.matrizX0 < dispositivo.matrizX:
                self.matrizX0 = dispositivo.matrizX
        elif dispositivo.orden == 1:
            if self.matrizY0 < dispositivo.matrizY:
                self.matrizY0 = dispositivo.matrizY
            if self.matrizX1 < dispositivo.matrizX:
                self.matrizX1 = dispositivo.matrizX
        elif dispositivo.orden == 2:
            if self.matrizY0 < dispositivo.matrizY:
                self.matrizY0 = dispositivo.matrizY
            if self.matrizX2 < dispositivo.matrizX:
                self.matrizX2 = dispositivo.matrizX
        elif dispositivo.orden == 3:
            if self.matrizY1 < dispositivo.matrizY:
                self.matrizY1 = dispositivo.matrizY
            if self.matrizX0 < dispositivo.matrizX:
                self.matrizX0 = dispositivo.matrizX
        elif dispositivo.orden == 4:
            if self.matrizY1 < dispositivo.matrizY:
                self.matrizY1 = dispositivo.matrizY
            if self.matrizX1 < dispositivo.matrizX:
                self.matrizX1 = dispositivo.matrizX
        elif dispositivo.orden == 5:
            if self.matrizY1 < dispositivo.matrizY:
                self.matrizY1 = dispositivo.matrizY
            if self.matrizX2 < dispositivo.matrizX:
                self.matrizX2 = dispositivo.matrizX
        elif dispositivo.orden == 6:
            if self.matrizY2 < dispositivo.matrizY:
                self.matrizY2 = dispositivo.matrizY
            if self.matrizX0 < dispositivo.matrizX:
                self.matrizX0 = dispositivo.matrizX
        elif dispositivo.orden == 7:
            if self.matrizY2 < dispositivo.matrizY:
                self.matrizY2 = dispositivo.matrizY
            if self.matrizX1 < dispositivo.matrizX:
                self.matrizX1 = dispositivo.matrizX
        elif dispositivo.orden == 8:
            if self.matrizY2 < dispositivo.matrizY:
                self.matrizY2 = dispositivo.matrizY
            if self.matrizX2 < dispositivo.matrizX:
                self.matrizX2 = dispositivo.matrizX

    def detener_dispositivos(self):
        for dispositivo in self.dispositivosActivos:
            dispositivo.detenerConexion()

    def iniciar_dispositivos(self):
        for dispositivo in self.dispositivosActivos:
            dispositivo.iniciarConexion()

    def print_cantidad_dispositivos_activos(self):
        print('Dispositivos Activos: ' + str(len(self.dispositivosActivos)))

    def print_dispositivos_activos(self):
        for disp in self.dispositivosActivos:
            print('Dispositivo = ip: ' + str(disp.ip) + ' universo: ' + str(disp.universo)
                  + ' orden: ' + str(disp.orden) + ' X: ' + str(disp.matrizX) + ' Y: ' + str(disp.matrizY))

    def buscar_o_agregar_dispositivo(self, ip, universo, patch, mx, my, orden, tipo_led):
        try:
            disp = [x for x in self.dispositivosActivos if x.ip == ip and x.universo == universo][0]
            return disp

        except IndexError:
            disp = dispositivo_artnet.DispositivoArtnet(ip, universo, patch, mx, my, orden, tipo_led)
            self.dispositivosActivos.append(disp)
            self.actualizar_maximo_matriz_x_matriz_y(disp)
            return disp

    def scroll(self, data_json):

        threads = list()

        velocidad = data_json['velocidad']
        direccion = data_json['direccion']

        while globales.REPETICION:
            for dispositivo in self.dispositivosActivos:
                if direccion == 'Derecha':
                    if dispositivo.contador == 12:
                        dispositivo.reiniciar_contador()

                    for i in range(dispositivo.matrizY):
                        for c in range(dispositivo.matrizX):

                            if dispositivo.orden == 1 or dispositivo.orden == 4 or dispositivo.orden == 7:
                                num_color = c + dispositivo.contador + self.matrizX0
                            elif dispositivo.orden == 2 or dispositivo.orden == 5 or dispositivo.orden == 8:
                                num_color = c + dispositivo.contador + self.matrizX0 + self.matrizX1
                            else:
                                num_color = c + dispositivo.contador

                            if num_color > 11:
                                for p in range(int(num_color / 11)):
                                    num_color = num_color - 12

                            led_rojo = int(self.coloresScroll[num_color][1] + self.coloresScroll[num_color][2], 16)
                            led_verde = int(self.coloresScroll[num_color][3] + self.coloresScroll[num_color][4], 16)
                            led_azul = int(self.coloresScroll[num_color][5] + self.coloresScroll[num_color][6], 16)

                            dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                    dispositivo.contador += 1

                elif direccion == 'Izquierda':
                    if dispositivo.contador == -1:
                        dispositivo.contador = 11

                    for i in range(dispositivo.matrizY):
                        for c in range(dispositivo.matrizX):

                            if dispositivo.orden == 1 or dispositivo.orden == 4 or dispositivo.orden == 7:
                                num_color = dispositivo.contador - c - self.matrizX0
                            elif dispositivo.orden == 2 or dispositivo.orden == 5 or dispositivo.orden == 8:
                                num_color = dispositivo.contador - c - self.matrizX0 - self.matrizX1
                            else:
                                num_color = dispositivo.contador - c

                            if num_color < 11:
                                for p in range(int(-num_color / 11)):
                                    num_color = num_color + 12

                            led_rojo = int(self.coloresScroll[num_color][1] + self.coloresScroll[num_color][2], 16)
                            led_verde = int(self.coloresScroll[num_color][3] + self.coloresScroll[num_color][4], 16)
                            led_azul = int(self.coloresScroll[num_color][5] + self.coloresScroll[num_color][6], 16)

                            dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                    dispositivo.contador -= 1

                elif direccion == 'Abajo':
                    if dispositivo.contador == 12:
                        dispositivo.reiniciar_contador()

                    for i in range(dispositivo.matrizY):

                        if dispositivo.orden == 3 or dispositivo.orden == 4 or dispositivo.orden == 5:
                            num_color = i + dispositivo.contador + self.matrizY0
                        elif dispositivo.orden == 6 or dispositivo.orden == 7 or dispositivo.orden == 8:
                            num_color = i + dispositivo.contador + self.matrizY0 + self.matrizY1
                        else:
                            num_color = i + dispositivo.contador

                        if num_color > 11:
                            for p in range(int(num_color / 11)):
                                num_color = num_color - 12

                        led_rojo = int(self.coloresScroll[num_color][1] + self.coloresScroll[num_color][2], 16)
                        led_verde = int(self.coloresScroll[num_color][3] + self.coloresScroll[num_color][4], 16)
                        led_azul = int(self.coloresScroll[num_color][5] + self.coloresScroll[num_color][6], 16)

                        for c in range(dispositivo.matrizX):
                            dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                    dispositivo.contador += 1

                elif direccion == 'Arriba':
                    if dispositivo.contador == 0:
                        dispositivo.contador = 11
                    for i in range(dispositivo.matrizY):

                        if dispositivo.orden == 3 or dispositivo.orden == 4 or dispositivo.orden == 5:
                            num_color = dispositivo.contador - i - self.matrizY0
                        elif dispositivo.orden == 6 or dispositivo.orden == 7 or dispositivo.orden == 8:
                            num_color = dispositivo.contador - i - self.matrizY0 - self.matrizY1
                        else:
                            num_color = dispositivo.contador - i

                        if num_color < 11:
                            for p in range(int(-num_color / 11)):
                                num_color = num_color + 12

                        led_rojo = int(self.coloresScroll[num_color][1] + self.coloresScroll[num_color][2], 16)
                        led_verde = int(self.coloresScroll[num_color][3] + self.coloresScroll[num_color][4], 16)
                        led_azul = int(self.coloresScroll[num_color][5] + self.coloresScroll[num_color][6], 16)

                        for c in range(dispositivo.matrizX):
                            dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                    dispositivo.contador -= 1

                threads.append(threading.Thread(target=dispositivo.enviar_datos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

            time.sleep(1 / int(velocidad))

    def scan(self, data_json):

        threads = list()

        velocidad = data_json['velocidad']
        direccion = data_json['direccion']
        color_scan = data_json['colorScan']
        color_fondo = data_json['colorFondo']

        while globales.REPETICION:
            for dispositivo in self.dispositivosActivos:
                # pongo el color de fondo
                for i in range(dispositivo.matrizX * dispositivo.matrizY):
                    led_rojo = int(color_fondo[1] + color_fondo[2], 16)
                    led_verde = int(color_fondo[3] + color_fondo[4], 16)
                    led_azul = int(color_fondo[5] + color_fondo[6], 16)

                    dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                # preparo el color del scan
                led_rojo = int(color_scan[1] + color_scan[2], 16)
                led_verde = int(color_scan[3] + color_scan[4], 16)
                led_azul = int(color_scan[5] + color_scan[6], 16)

                if direccion == 'Abajo':
                    # Reinicia el contador
                    if dispositivo.contador == dispositivo.matrizX * dispositivo.matrizY * 3:
                        dispositivo.contador = 0

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizX):
                        num = i * 3
                        dispositivo.datosAEnviar[dispositivo.contador + num] = led_rojo
                        dispositivo.datosAEnviar[dispositivo.contador + 1 + num] = led_verde
                        dispositivo.datosAEnviar[dispositivo.contador + 2 + num] = led_azul

                    dispositivo.contador += dispositivo.matrizX * 3

                elif direccion == 'Izquierda':
                    # Reinicia el contador
                    if dispositivo.contador == 0:
                        dispositivo.contador = dispositivo.matrizX * 3

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizY):
                        num = i * 3 * dispositivo.matrizX + 1
                        dispositivo.datosAEnviar[dispositivo.contador - 2 - num] = led_rojo
                        dispositivo.datosAEnviar[dispositivo.contador - 1 - num] = led_verde
                        dispositivo.datosAEnviar[dispositivo.contador - num] = led_azul

                    dispositivo.contador -= 3

                elif direccion == 'Arriba':
                    # Reinicia el contador
                    if dispositivo.contador == 0:
                        dispositivo.contador = dispositivo.matrizY * dispositivo.matrizX * 3

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizX):
                        num = i * 3 + 1
                        dispositivo.datosAEnviar[dispositivo.contador - 2 - num] = led_rojo
                        dispositivo.datosAEnviar[dispositivo.contador - 1 - num] = led_verde
                        dispositivo.datosAEnviar[dispositivo.contador - num] = led_azul

                    dispositivo.contador -= dispositivo.matrizX * 3

                elif direccion == 'Derecha':

                    if dispositivo.contador == dispositivo.matrizX * 3:
                        dispositivo.reiniciar_contador()

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizY):
                        num = i * 3 * dispositivo.matrizX
                        dispositivo.datosAEnviar[dispositivo.contador + num] = led_rojo
                        dispositivo.datosAEnviar[dispositivo.contador + 1 + num] = led_verde
                        dispositivo.datosAEnviar[dispositivo.contador + 2 + num] = led_azul

                    dispositivo.contador += 3

                threads.append(threading.Thread(target=dispositivo.enviar_datos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

            time.sleep(1 / int(velocidad))

    def estrellas(self, data_json):
        velocidad = data_json['velocidad']
        color_estrellas = data_json['colorEstrellas']
        color_fondo = data_json['colorFondo']

        threads = list()

        while globales.REPETICION:
            # pongo el color de fondo
            for dispositivo in self.dispositivosActivos:
                for i in range(dispositivo.matrizX * dispositivo.matrizY):
                    led_rojo = int(color_fondo[1] + color_fondo[2], 16)
                    led_verde = int(color_fondo[3] + color_fondo[4], 16)
                    led_azul = int(color_fondo[5] + color_fondo[6], 16)

                    dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                # preparo el color de las estrellas
                led_rojo = int(color_estrellas[1] + color_estrellas[2], 16)
                led_verde = int(color_estrellas[3] + color_estrellas[4], 16)
                led_azul = int(color_estrellas[5] + color_estrellas[6], 16)

                cantidad_estrellas = int(dispositivo.matrizX * dispositivo.matrizY / 3)

                for c in range(cantidad_estrellas):
                    num_max = dispositivo.matrizX * dispositivo.matrizY - 1
                    numero_random = random.randint(0, num_max)

                    dispositivo.datosAEnviar[numero_random * 3] = led_rojo
                    dispositivo.datosAEnviar[numero_random * 3 + 1] = led_verde
                    dispositivo.datosAEnviar[numero_random * 3 + 2] = led_azul

                threads.append(threading.Thread(target=dispositivo.enviar_datos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

            time.sleep(3 / int(velocidad))

    def color(self, data_json):
        color = data_json['color']
        velocidad = data_json['velocidad']
        cambio_constante = data_json['cambio_constante']

        threads = list()

        if 'checked' == cambio_constante:
            led_actual = 0
            while globales.REPETICION:
                # Usar módulo para mantener el contador dentro del rango de la lista
                color = self.coloresScroll[led_actual % len(self.coloresScroll)]

                for dispositivo in self.dispositivosActivos:
                    for c in range(dispositivo.matrizX * dispositivo.matrizY):
                        led_rojo = int(color[1] + color[2], 16)
                        led_verde = int(color[3] + color[4], 16)
                        led_azul = int(color[5] + color[6], 16)

                        dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                    threads.append(threading.Thread(target=dispositivo.enviar_datos, daemon=True))

                for thread in threads:
                    thread.start()

                threads.clear()

                time.sleep(3 / int(velocidad))

                led_actual += 1
        else:
            for dispositivo in self.dispositivosActivos:
                for c in range(dispositivo.matrizX * dispositivo.matrizY):
                    led_rojo = int(color[1] + color[2], 16)
                    led_verde = int(color[3] + color[4], 16)
                    led_azul = int(color[5] + color[6], 16)

                    dispositivo.datosAEnviar.extend([led_rojo, led_verde, led_azul])

                threads.append(threading.Thread(target=dispositivo.enviar_datos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

    def probar_dispositivo(self):
        for dispositivo in self.dispositivosActivos:
            for x in range(512):
                dispositivo.datosAEnviar.append(255)
            dispositivo.enviar_datos()
            time.sleep(3)
            dispositivo.conexionArtnet.blackout()
