import random
import threading
import time

import dispositivo_artnet
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

    def actualizarMaximoMatrizXMatrizY(self, dispositivo):
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

    def detenerDispositivos(self):
        for dispositivo in self.dispositivosActivos:
            dispositivo.detenerConexion()

    def iniciarDispositivos(self):
        for dispositivo in self.dispositivosActivos:
            dispositivo.iniciarConexion()

    def printCantidadDispositivosActivos(self):
        print('Dispositivos Activos: ' + str(len(self.dispositivosActivos)))

    def printDispositivosActivos(self):
        for disp in self.dispositivosActivos:
            print('Dispositivo = ip: ' + str(disp.ip) + ' universo: ' + str(disp.universo)
                  + ' orden: ' + str(disp.orden) + ' X: ' + str(disp.matrizX) + ' Y: ' + str(disp.matrizY))

    def buscarOAgregarDispositivo(self, ip, universo, patch, mx, my, orden, tipoLed):
        try:
            disp = [x for x in self.dispositivosActivos if x.ip == ip and x.universo == universo][0]
            return disp

        except IndexError:
            disp = dispositivo_artnet.DispositivoArtnet(ip, universo, patch, mx, my, orden, tipoLed)
            self.dispositivosActivos.append(disp)
            self.actualizarMaximoMatrizXMatrizY(disp)
            return disp

    def scroll(self, dataJson):

        threads = list()

        velocidad = dataJson['velocidad']
        direccion = dataJson['direccion']

        while globales.REPETICION:
            for dispositivo in self.dispositivosActivos:
                if direccion == 'Derecha':
                    if dispositivo.contador == 12:
                        dispositivo.reiniciarContador()

                    for i in range(dispositivo.matrizY):
                        for c in range(dispositivo.matrizX):

                            if dispositivo.orden == 1 or dispositivo.orden == 4 or dispositivo.orden == 7:
                                numColor = c + dispositivo.contador + self.matrizX0
                            elif dispositivo.orden == 2 or dispositivo.orden == 5 or dispositivo.orden == 8:
                                numColor = c + dispositivo.contador + self.matrizX0 + self.matrizX1
                            else:
                                numColor = c + dispositivo.contador

                            if numColor > 11:
                                for p in range(int(numColor / 11)):
                                    numColor = numColor - 12

                            ledRojo = int(self.coloresScroll[numColor][1] + self.coloresScroll[numColor][2], 16)
                            ledVerde = int(self.coloresScroll[numColor][3] + self.coloresScroll[numColor][4], 16)
                            ledAzul = int(self.coloresScroll[numColor][5] + self.coloresScroll[numColor][6], 16)

                            dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

                    dispositivo.contador += 1

                elif direccion == 'Izquierda':
                    if dispositivo.contador == -1:
                        dispositivo.contador = 11

                    for i in range(dispositivo.matrizY):
                        for c in range(dispositivo.matrizX):

                            if dispositivo.orden == 1 or dispositivo.orden == 4 or dispositivo.orden == 7:
                                numColor = dispositivo.contador - c - self.matrizX0
                            elif dispositivo.orden == 2 or dispositivo.orden == 5 or dispositivo.orden == 8:
                                numColor = dispositivo.contador - c - self.matrizX0 - self.matrizX1
                            else:
                                numColor = dispositivo.contador - c

                            if numColor < 11:
                                for p in range(int(-numColor / 11)):
                                    numColor = numColor + 12

                            ledRojo = int(self.coloresScroll[numColor][1] + self.coloresScroll[numColor][2], 16)
                            ledVerde = int(self.coloresScroll[numColor][3] + self.coloresScroll[numColor][4], 16)
                            ledAzul = int(self.coloresScroll[numColor][5] + self.coloresScroll[numColor][6], 16)

                            dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

                    dispositivo.contador -= 1

                elif direccion == 'Abajo':
                    if dispositivo.contador == 12:
                        dispositivo.reiniciarContador()

                    for i in range(dispositivo.matrizY):

                        if dispositivo.orden == 3 or dispositivo.orden == 4 or dispositivo.orden == 5:
                            numColor = i + dispositivo.contador + self.matrizY0
                        elif dispositivo.orden == 6 or dispositivo.orden == 7 or dispositivo.orden == 8:
                            numColor = i + dispositivo.contador + self.matrizY0 + self.matrizY1
                        else:
                            numColor = i + dispositivo.contador

                        if numColor > 11:
                            for p in range(int(numColor / 11)):
                                numColor = numColor - 12

                        ledRojo = int(self.coloresScroll[numColor][1] + self.coloresScroll[numColor][2], 16)
                        ledVerde = int(self.coloresScroll[numColor][3] + self.coloresScroll[numColor][4], 16)
                        ledAzul = int(self.coloresScroll[numColor][5] + self.coloresScroll[numColor][6], 16)

                        for c in range(dispositivo.matrizX):
                            dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

                    dispositivo.contador += 1

                elif direccion == 'Arriba':
                    if dispositivo.contador == 0:
                        dispositivo.contador = 11
                    for i in range(dispositivo.matrizY):

                        if dispositivo.orden == 3 or dispositivo.orden == 4 or dispositivo.orden == 5:
                            numColor = dispositivo.contador - i - self.matrizY0
                        elif dispositivo.orden == 6 or dispositivo.orden == 7 or dispositivo.orden == 8:
                            numColor = dispositivo.contador - i - self.matrizY0 - self.matrizY1
                        else:
                            numColor = dispositivo.contador - i

                        if numColor < 11:
                            for p in range(int(-numColor / 11)):
                                numColor = numColor + 12

                        ledRojo = int(self.coloresScroll[numColor][1] + self.coloresScroll[numColor][2], 16)
                        ledVerde = int(self.coloresScroll[numColor][3] + self.coloresScroll[numColor][4], 16)
                        ledAzul = int(self.coloresScroll[numColor][5] + self.coloresScroll[numColor][6], 16)

                        for c in range(dispositivo.matrizX):
                            dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

                    dispositivo.contador -= 1

                threads.append(threading.Thread(target=dispositivo.enviarDatos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

            time.sleep(1 / int(velocidad))

    def scan(self, dataJson):

        threads = list()

        posicion = 0

        velocidad = dataJson['velocidad']
        direccion = dataJson['direccion']
        colorScan = dataJson['colorScan']
        colorFondo = dataJson['colorFondo']

        while globales.REPETICION:
            for dispositivo in self.dispositivosActivos:
                # pongo el color de fondo
                for i in range(dispositivo.matrizX * dispositivo.matrizY):
                    ledRojo = int(colorFondo[1] + colorFondo[2], 16)
                    ledVerde = int(colorFondo[3] + colorFondo[4], 16)
                    ledAzul = int(colorFondo[5] + colorFondo[6], 16)

                    dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

                # preparo el color del scan
                ledRojo = int(colorScan[1] + colorScan[2], 16)
                ledVerde = int(colorScan[3] + colorScan[4], 16)
                ledAzul = int(colorScan[5] + colorScan[6], 16)

                if direccion == 'Abajo':
                    # Reinicia el contador
                    if dispositivo.contador == dispositivo.matrizX * dispositivo.matrizY * 3:
                        dispositivo.contador = 0

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizX):
                        num = i * 3
                        dispositivo.datosAEnviar[dispositivo.contador + num] = ledRojo
                        dispositivo.datosAEnviar[dispositivo.contador + 1 + num] = ledVerde
                        dispositivo.datosAEnviar[dispositivo.contador + 2 + num] = ledAzul

                    dispositivo.contador += dispositivo.matrizX * 3

                elif direccion == 'Izquierda':
                    # Reinicia el contador
                    if dispositivo.contador == 0:
                        dispositivo.contador = dispositivo.matrizX * 3

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizY):
                        num = i * 3 * dispositivo.matrizX + 1
                        dispositivo.datosAEnviar[dispositivo.contador - 2 - num] = ledRojo
                        dispositivo.datosAEnviar[dispositivo.contador - 1 - num] = ledVerde
                        dispositivo.datosAEnviar[dispositivo.contador - num] = ledAzul

                    dispositivo.contador -= 3

                elif direccion == 'Arriba':
                    # Reinicia el contador
                    if dispositivo.contador == 0:
                        dispositivo.contador = dispositivo.matrizY * dispositivo.matrizX * 3

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizX):
                        num = i * 3 + 1
                        dispositivo.datosAEnviar[dispositivo.contador - 2 - num] = ledRojo
                        dispositivo.datosAEnviar[dispositivo.contador - 1 - num] = ledVerde
                        dispositivo.datosAEnviar[dispositivo.contador - num] = ledAzul

                    dispositivo.contador -= dispositivo.matrizX * 3

                elif direccion == 'Derecha':

                    # print(str(self.matrizX0) + ' ' + str(self.matrizX1) + ' ' + str(self.matrizX2))
                    # print(str(self.matrizY0) + ' ' + str(self.matrizY1) + ' ' + str(self.matrizY2))
                    #
                    # if posicion > (self.matrizX0 + self.matrizX1 + self.matrizX2) * 3:
                    #     posicion = 0
                    #
                    # for i in range(dispositivo.matrizY):
                    #     num = i * 3 * dispositivo.matrizX
                    #     dispositivo.datosAEnviar[posicion + num] = ledRojo
                    #     dispositivo.datosAEnviar[posicion + 1 + num] = ledVerde
                    #     dispositivo.datosAEnviar[posicion + 2 + num] = ledAzul
                    #
                    # posicion += 3

                    if dispositivo.contador == dispositivo.matrizX * 3:
                        dispositivo.reiniciarContador()

                    # a la lista de leds le cambio los leds que usa el scan
                    for i in range(dispositivo.matrizY):
                        num = i * 3 * dispositivo.matrizX
                        dispositivo.datosAEnviar[dispositivo.contador + num] = ledRojo
                        dispositivo.datosAEnviar[dispositivo.contador + 1 + num] = ledVerde
                        dispositivo.datosAEnviar[dispositivo.contador + 2 + num] = ledAzul

                    dispositivo.contador += 3

                threads.append(threading.Thread(target=dispositivo.enviarDatos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

            time.sleep(1 / int(velocidad))

    def estrellas(self, dataJson):
        velocidad = dataJson['velocidad']
        colorEstrellas = dataJson['colorEstrellas']
        colorFondo = dataJson['colorFondo']

        threads = list()

        while globales.REPETICION:
            # pongo el color de fondo
            for dispositivo in self.dispositivosActivos:
                for i in range(dispositivo.matrizX * dispositivo.matrizY):
                    ledRojo = int(colorFondo[1] + colorFondo[2], 16)
                    ledVerde = int(colorFondo[3] + colorFondo[4], 16)
                    ledAzul = int(colorFondo[5] + colorFondo[6], 16)

                    dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

                # preparo el color de las estrellas
                ledRojo = int(colorEstrellas[1] + colorEstrellas[2], 16)
                ledVerde = int(colorEstrellas[3] + colorEstrellas[4], 16)
                ledAzul = int(colorEstrellas[5] + colorEstrellas[6], 16)

                cantidadEstrellas = int(dispositivo.matrizX * dispositivo.matrizY / 3)

                for c in range(cantidadEstrellas):
                    numMax = dispositivo.matrizX * dispositivo.matrizY - 1
                    numeroRandom = random.randint(0, numMax)

                    dispositivo.datosAEnviar[numeroRandom * 3] = ledRojo
                    dispositivo.datosAEnviar[numeroRandom * 3 + 1] = ledVerde
                    dispositivo.datosAEnviar[numeroRandom * 3 + 2] = ledAzul

                threads.append(threading.Thread(target=dispositivo.enviarDatos, daemon=True))

            for thread in threads:
                thread.start()

            threads.clear()

            time.sleep(3 / int(velocidad))

    def color(self, dataJson):
        color = dataJson['color']
        threads = list()

        for dispositivo in self.dispositivosActivos:
            for c in range(dispositivo.matrizX * dispositivo.matrizY * 3):
                ledRojo = int(color[1] + color[2], 16)
                ledVerde = int(color[3] + color[4], 16)
                ledAzul = int(color[5] + color[6], 16)

                dispositivo.datosAEnviar.extend([ledRojo, ledVerde, ledAzul])

            threads.append(threading.Thread(target=dispositivo.enviarDatos, daemon=True))

        for thread in threads:
            thread.start()

    def probarDispositivo(self):
        for dispositivo in self.dispositivosActivos:
            for x in range(512):
                dispositivo.datosAEnviar.append(255)
            dispositivo.enviarDatos()
            time.sleep(3)
            dispositivo.conexionArtnet.blackout()
