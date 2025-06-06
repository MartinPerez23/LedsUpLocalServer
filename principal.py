import asyncio
import json
import os
import queue
import threading
import time
from datetime import datetime

import customtkinter as ctk
import websockets

import conexion_artnet
import globales
import login

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

appWidth, appHeight = 600, 400

TOKEN = os.environ.get('TOKEN')
WS_URI = "wss://ledsupwebserver.onrender.com/ledsup/wsremoteandlocal/"
WS_HEADERS = [
    ("Origin", "https://ledsupwebserver.onrender.com"),
    ("Authorization", f"Token {TOKEN}")
]

comando_queue = queue.Queue()
ws_stop_event = threading.Event()


def detenerTheadsViejos():
    globales.REPETICION = False
    time.sleep(2)
    globales.REPETICION = True


class ControladorLEDs:
    def __init__(self):
        self.artnet = conexion_artnet.ConexionArtnet()

    def procesar_comando(self, dataJson, app_view):
        app_view.print_console("Comando recibido:" + str(dataJson))
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
            t = threading.Thread(target=self.artnet.color, args=(dataJson,), daemon=True)
            t.start()

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


async def escuchar_websocket(app_view):
    try:
        async with websockets.connect(WS_URI, extra_headers=WS_HEADERS) as websocket:
            app_view.print_console("Conectado al servidor Web")
            while True:
                mensaje = await websocket.recv()
                data = json.loads(mensaje)
                comando = data.get('data')

                if comando:
                    comando_queue.put(comando)
                    await websocket.send(json.dumps({"estado": "ok"}))
                else:
                    app_view.print_console(
                        "Formato inesperado:" + str(data) + "\n")  # todo crear Error en Base de datos

    except Exception as e:
        print(e)
        app_view.print_console("Error: contactar con soporte.\n")
        app_view.ConnectButton._clicked()


def procesar_comandos_thread(controlador: ControladorLEDs, app_view):
    while True:
        comando = comando_queue.get()
        if comando is None:
            break
        controlador.procesar_comando(comando, app_view)


class AppView(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Led's up")
        self.geometry("600x400")

        self.displayBox = ctk.CTkTextbox(self, width=300, height=250)
        self.displayBox.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsw")
        self.displayBox.configure(state="disabled")

        self.rightFrame = ctk.CTkFrame(self)
        self.rightFrame.grid(row=0, column=1, rowspan=3, padx=20, pady=20, sticky="nsew")

        self.statusLabel = ctk.CTkLabel(self.rightFrame, text="Estado:")
        self.statusLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.statusEntry = ctk.CTkEntry(self.rightFrame, state='disabled')
        self.statusEntry.grid(row=0, column=1, padx=10, pady=10)
        self.set_status_entry("Desconectado", "red")

        self.userLabel = ctk.CTkLabel(self.rightFrame, text="Usuario:")
        self.userLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.userEntry = ctk.CTkEntry(self.rightFrame, state='disabled')
        self.userEntry.grid(row=1, column=1, padx=10, pady=10)
        self.get_user_entry()

        self.ConnectButton = ctk.CTkButton(self.rightFrame, text="Conectar", command=self.change_status)
        self.ConnectButton.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_columnconfigure(1, weight=1)

        self.hilo_ws = None

    def get_user_entry(self):
        self.userEntry.configure(state="normal")
        self.userEntry.insert(0, "JOSE")
        self.userEntry.configure(state="disabled")

    def set_status_entry(self, texto, color):
        self.statusEntry.configure(state="normal")
        self.statusEntry.delete(0, "end")
        self.statusEntry.insert(0, texto)
        self.statusEntry.configure(state="disabled", text_color=color)

    def print_console(self, text):
        text = f"[{datetime.now().strftime('%d/%m %H:%M')}] " + text + "\n"

        self.displayBox.configure(state="normal")
        self.displayBox.insert("0.0", text)
        self.displayBox.configure(state="disabled")

    def change_status(self):
        global ws_stop_event

        if self.statusEntry.get() == "Desconectado":
            self.set_status_entry("Conectado", "green")
            self.ConnectButton.configure(text="Desconectar")

            ws_stop_event.clear()

            controlador = ControladorLEDs()

            hilo_procesador = threading.Thread(target=procesar_comandos_thread, args=(controlador, self), daemon=True)

            hilo_procesador.start()

            def iniciar_websocket():
                asyncio.run(escuchar_websocket(self))

            self.hilo_ws = threading.Thread(target=iniciar_websocket, daemon=True)
            self.hilo_ws.start()

        else:
            self.set_status_entry("Desconectado", "red")
            self.ConnectButton.configure(text="Conectar")
            self.print_console("Desconectado de la web")

            ws_stop_event.set()


if __name__ == "__main__":
    app = login.Login()
    app.mainloop()

    app = AppView()
    app.mainloop()
