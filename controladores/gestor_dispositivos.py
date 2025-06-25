# controladores/gestordispositivos.py
from modelo.dispositivo_artnet import DispositivoArtnet

class GestorDispositivos:
    def __init__(self):
        self.dispositivos_activos = []

    def actualizar_lista(self, lista_dispositivos):
        nuevas_claves = {(d['ip'], d['universo']) for d in lista_dispositivos}
        actuales_claves = {(d.ip, d.universo) for d in self.dispositivos_activos}

        # Cerrar y eliminar dispositivos que ya no están
        for dispositivo in self.dispositivos_activos:
            if (dispositivo.ip, dispositivo.universo) not in nuevas_claves:
                dispositivo.detener_conexion()

        self.dispositivos_activos = [d for d in self.dispositivos_activos
                                     if (d.ip, d.universo) in nuevas_claves]

        # Agregar nuevos dispositivos
        for d in lista_dispositivos:
            if (d['ip'], d['universo']) not in actuales_claves:
                nuevo = DispositivoArtnet(
                    d['ip'], d['universo'], d['patch'],
                    d['matriz_x'], d['matriz_y'], d['orden'], d['tipo_led']
                )
                nuevo.iniciar_conexion()
                self.dispositivos_activos.append(nuevo)

        self.dispositivos_activos.sort(key=lambda d: d.orden)

    def detener_todas(self):
        for d in self.dispositivos_activos:
            d.detener_conexion()

    def obtener_dispositivos(self):
        return self.dispositivos_activos
