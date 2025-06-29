from stupidArtnet import StupidArtnet


class DispositivoArtnet:
    def __init__(self, ip, universo, patch, matriz_x, matriz_y, orden, tipo_led):
        self.ip = ip
        self.universo = universo
        self.patch = patch
        self.matrizX = matriz_x
        self.matrizY = matriz_y
        self.orden = orden
        self.tipoLed = tipo_led
        self.datosAEnviar = []
        self.contador = 0
        self.conexionArtnet = StupidArtnet(ip, universo, 512, 30, True, True)

    def reiniciar_contador(self):
        self.contador = 0

    def iniciar_conexion(self):
        self.conexionArtnet.start()

    def detener_conexion(self):
        self.conexionArtnet.stop()

    def enviar_datos(self):
        leds = [0] * 512
        datos = self.datosAEnviar[:512]

        if self.patch and self.patch not in ['Sin patch', '']:
            patch = [int(x) for x in self.patch.split(',')]
            for i, pos in enumerate(patch):
                if i * 3 + 2 >= len(self.datosAEnviar):
                    continue
                r, g, b = self.reordenar(i)
                leds[pos * 3:pos * 3 + 3] = [r, g, b]
        else:
            leds[:len(datos)] = datos

        self.conexionArtnet.set(leds)

    def reordenar(self, i):
        r, g, b = self.datosAEnviar[i * 3:i * 3 + 3]
        orden = self.tipoLed
        if orden == 'RGB': return r, g, b
        if orden == 'RBG': return r, b, g
        if orden == 'GRB': return g, r, b
        if orden == 'GBR': return g, b, r
        if orden == 'BRG': return b, r, g
        if orden == 'BGR': return b, g, r
        return r, g, b
