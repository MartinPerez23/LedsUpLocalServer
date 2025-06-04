import asyncio
import json
import threading
import time
import websockets
import queue
from Lib import os

import ssl
import conexion_artnet
import globales

ssl_context = ssl._create_unverified_context()
TOKEN = os.environ.get('token')
WS_URI = "wss://localhost:8000/ledsup/wsremoteandlocal/"
WS_HEADERS = [
    ("Origin", "https://localhost:8000"),
    ("Authorization", f"Token {TOKEN}")
]

comando_queue = queue.Queue()


def detenerTheadsViejos():
    globales.REPETICION = False
    time.sleep(2)
    globales.REPETICION = True


class ControladorLEDs:
    def __init__(self):
        self.artnet = conexion_artnet.ConexionArtnet()

    def procesar_comando(self, dataJson):
        print("Comando recibido:", dataJson)
        self.artnet.dispositivosActivos.clear()
        accion = dataJson['accion']
        dispositivosActuales = dataJson['lista']
        numeroDispositivos = int(len(dispositivosActuales) / 6)

        for repeticion in range(numeroDispositivos):
            numero = repeticion * 7
            ip = dispositivosActuales[numero]
            universo = int(dispositivosActuales[numero + 1])
            matrizX = int(dispositivosActuales[numero + 2])
            matrizY = int(dispositivosActuales[numero + 3])
            patch = dispositivosActuales[numero + 4]
            orden = dispositivosActuales[numero + 5]
            tipoLed = dispositivosActuales[numero + 6]

            orden_map = {
                'Arriba-Izquierda': 0, 'Arriba': 1, 'Arriba-Derecha': 2,
                'Izquierda': 3, 'Centro': 4, 'Derecha': 5,
                'Abajo-Izquierda': 6, 'Abajo': 7, 'Abajo-Derecha': 8
            }
            orden = orden_map.get(orden, 4)

            self.artnet.buscarOAgregarDispositivo(ip, universo, patch, matrizX, matrizY, orden, tipoLed)

        self.artnet.dispositivosActivos = sorted(
            self.artnet.dispositivosActivos, key=lambda d: d.orden
        )

        self.artnet.printCantidadDispositivosActivos()
        self.artnet.printDispositivosActivos()

        if accion == 'probar':
            detenerTheadsViejos()
            self.artnet.probarDispositivo()

        elif accion == 'color':
            detenerTheadsViejos()
            self.artnet.color(dataJson)

        elif accion == 'scroll':
            detenerTheadsViejos()
            t = threading.Thread(target=self.artnet.scroll, args=(dataJson,), daemon=True)
            t.start()

        elif accion == 'scan':
            detenerTheadsViejos()
            t = threading.Thread(target=self.artnet.scan, args=(dataJson,), daemon=True)
            t.start()

        elif accion == 'estrellas':
            detenerTheadsViejos()
            t = threading.Thread(target=self.artnet.estrellas, args=(dataJson,), daemon=True)
            t.start()


async def escuchar_websocket():
    try:
        async with websockets.connect(WS_URI, extra_headers=WS_HEADERS, ssl=ssl_context) as websocket:
            print("Conectado al servidor Django (WebSocket)")
            while True:
                mensaje = await websocket.recv()
                data = json.loads(mensaje)
                comando = data.get('data')

                if comando:
                    comando_queue.put(comando)  # Enviamos el comando al otro thread
                    await websocket.send(json.dumps({"estado": "ok"}))
                else:
                    print("Formato inesperado:", data)

    except Exception as e:
        print("Error en WebSocket:", e)


def procesar_comandos_thread(controlador: ControladorLEDs):
    while True:
        comando = comando_queue.get()  # Espera bloqueante
        if comando is None:
            break  # Salida segura
        controlador.procesar_comando(comando)


if __name__ == "__main__":
    controlador = ControladorLEDs()

    # Thread que procesa los comandos
    hilo_procesador = threading.Thread(target=procesar_comandos_thread, args=(controlador,), daemon=True)
    hilo_procesador.start()

    # Arranca el loop async del websocket
    asyncio.run(escuchar_websocket())
