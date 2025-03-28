import time

from stupidArtnet import *


class DispositivoArtnet:
    def __init__(self, ip, universo, patch, matrizX, matrizY, orden, tipoLed):
        self.ip = ip
        self.universo = universo
        self.patch = patch
        self.matrizX = matrizX
        self.matrizY = matrizY
        self.orden = orden
        self.tipoLed = tipoLed
        self.datosAEnviar = list()
        self.contador = 0

        self.conexionArtnet = StupidArtnet(ip, int(universo), 512, 30, True, True)

    def reiniciarContador(self):
        self.contador = 0

    def iniciarConexion(self):
        self.conexionArtnet.start()

    def detenerConexion(self):
        self.conexionArtnet.stop()

    def enviarDatos(self):
        ledsPatcheados = self.datosAEnviar.copy()

        if self.patch != 'Sin patch':
            patch = [int(x) for x in self.patch.split(',')]
            for indice, posicion in enumerate(patch):
                if self.tipoLed == 'RGB':
                    ledsPatcheados[posicion * 3] = self.datosAEnviar[indice * 3]
                    ledsPatcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 1]
                    ledsPatcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 2]
                elif self.tipoLed == 'RBG':
                    ledsPatcheados[posicion * 3] = self.datosAEnviar[indice * 3]
                    ledsPatcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 2]
                    ledsPatcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 1]
                elif self.tipoLed == 'BRG':
                    ledsPatcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 2]
                    ledsPatcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3]
                    ledsPatcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 1]
                elif self.tipoLed == 'BGR':
                    ledsPatcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 2]
                    ledsPatcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 1]
                    ledsPatcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3]
                elif self.tipoLed == 'GRB':
                    ledsPatcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 1]
                    ledsPatcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3]
                    ledsPatcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3 + 2]
                elif self.tipoLed == 'GBR':
                    ledsPatcheados[posicion * 3] = self.datosAEnviar[indice * 3 + 1]
                    ledsPatcheados[posicion * 3 + 1] = self.datosAEnviar[indice * 3 + 2]
                    ledsPatcheados[posicion * 3 + 2] = self.datosAEnviar[indice * 3]

        if len(ledsPatcheados) <= 512:
            num = 512 - len(ledsPatcheados)
            for i in range(num):
                ledsPatcheados.append(0)
        else:
            ledsPatcheados.clear()
            for i in range(512):
                ledsPatcheados.append(30)

        self.datosAEnviar.clear()
        self.iniciarConexion()
        self.conexionArtnet.set(ledsPatcheados)
        print(
            'Enviado a ip: ' + self.conexionArtnet.target_ip + ' universo: ' + str(self.conexionArtnet.universe) + ': ')
        self.conexionArtnet.see_buffer()
        time.sleep(.2)
        ledsPatcheados.clear()
        self.detenerConexion()
