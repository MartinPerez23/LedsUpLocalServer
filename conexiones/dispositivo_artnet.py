import time

from stupidArtnet import *


class DispositivoArtnet:
    def __init__(self, ip, universo, patch, matriz_x, matriz_y, orden, tipo_led):
        self.ip = ip
        self.universo = universo
        self.patch = patch
        self.matrizX = matriz_x
        self.matrizY = matriz_y
        self.orden = orden
        self.tipoLed = tipo_led
        self.datosAEnviar = list()
        self.contador = 0

        self.conexionArtnet = StupidArtnet(ip, int(universo), 512, 30, True, True)

    def reiniciar_contador(self):
        self.contador = 0

    def iniciar_conexion(self):
        self.conexionArtnet.start()

    def detener_conexion(self):
        self.conexionArtnet.stop()

    def enviar_datos(self):
        leds_patcheados = self.datosAEnviar.copy()

        if self.patch not in ['Sin patch', '']:
            patch = [int(x) for x in self.patch.split(',')]
            for indice, posicion in enumerate(patch):
                if self.tipoLed == 'RGB':
                    leds_patcheados[posicion * 3] = self.datosAEnviar[indice * 3]
                    leds_patcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 1]
                    leds_patcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 2]
                elif self.tipoLed == 'RBG':
                    leds_patcheados[posicion * 3] = self.datosAEnviar[indice * 3]
                    leds_patcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 2]
                    leds_patcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 1]
                elif self.tipoLed == 'BRG':
                    leds_patcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 2]
                    leds_patcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3]
                    leds_patcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 1]
                elif self.tipoLed == 'BGR':
                    leds_patcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 2]
                    leds_patcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 1]
                    leds_patcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3]
                elif self.tipoLed == 'GRB':
                    leds_patcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 1]
                    leds_patcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3]
                    leds_patcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 2]
                elif self.tipoLed == 'GBR':
                    leds_patcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 1]
                    leds_patcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 2]
                    leds_patcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3]

        if len(leds_patcheados) <= 512:
            num = 512 - len(leds_patcheados)
            for i in range(num):
                leds_patcheados.append(0)
        else:
            leds_patcheados.clear()
            for i in range(512):
                leds_patcheados.append(30)

        self.datosAEnviar.clear()
        self.iniciar_conexion()
        self.conexionArtnet.set(leds_patcheados)
        print('Enviado a ip: ' + self.conexionArtnet.target_ip +
              ' universo: ' + str(self.conexionArtnet.universe) + ': ')
        self.conexionArtnet.see_buffer()
        time.sleep(.2)
        leds_patcheados.clear()
        self.detener_conexion()
