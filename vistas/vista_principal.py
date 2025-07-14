import asyncio
import json
import os
import queue
import ssl
import threading
import traceback

import customtkinter as ctk
import websockets

from auth_token.oauth_token_server import TokenManager
from controladores.controlador_errores import ControladorErrores
from controladores.controlador_leds import ControladorLEDs, detener_theads_viejos
from controladores.controlador_usuario import ControladorUsuario
from globales import resource_path
from modelos.modelo_error import ModeloError
from vistas.vista_popup_mensaje import PopupMensaje

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

comando_queue = queue.Queue()
ssl_context = ssl.create_default_context()


async def escuchar_websocket(app_view, stop_event: asyncio.Event):
    try:
        token = TokenManager.get_token()
        header = [
            ("Origin", os.environ.get('ORIGIN')),
            ("Authorization", f"Bearer {token}")
        ]

        async with websockets.connect(os.environ.get('WS_URI'), extra_headers=header, ssl=ssl_context) as websocket:
            print("conectado a websocket")
            app_view.set_status_entry("Conectado", "green")
            app_view.ConnectButton.configure(text="Desconectar", state="normal")

            asyncio.create_task(enviar_heartbeat(websocket, stop_event, app_view))

            while not stop_event.is_set():
                try:
                    mensaje = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(mensaje)
                    comando = data.get('data')

                    if comando:
                        print("Mensaje Recibido")
                        comando_queue.put(comando)
                        await websocket.send(json.dumps({"estado": "ok"}))
                    else:
                        PopupMensaje(app_view, "Se recibió un comando inesperado desde la web, vuelva a intentarlo",
                                     True)
                        app_view.reportar_error('Al recibir comando inesperando desde la web',
                                                "Formato inesperado:" + str(data))

                except asyncio.TimeoutError:
                    print("Esperando mensaje")
                    continue

    except Exception as e:
        print("Error en websocket", e)
        traceback.print_exc()

        app_view.reportar_error("Error en websocket", traceback.format_exc())
        app_view.set_status_entry("Desconectado", "red")
        app_view.ConnectButton.configure(text="Conectar", state="normal")
    finally:
        if websocket:
            await websocket.close()
            print("websocket desconectado")


def procesar_comandos_thread(controlador: ControladorLEDs, app_view):
    while True:
        comando = comando_queue.get()
        if comando is None:
            break
        controlador.procesar_comando(comando, app_view)


async def enviar_heartbeat(ws, stop_event, app_view):
    try:
        while not stop_event.is_set():
            await asyncio.sleep(10)  # cada 10 segundos
            await ws.send(json.dumps({"type": "ping"}))
    except Exception as e:
        print("Error al enviar heartbeat:", e)
        traceback.print_exc()
        app_view.reportar_error("Error al enviar heartbeat", traceback.format_exc())
        app_view.set_status_entry("Desconectado", "red")
        app_view.ConnectButton.configure(text="Conectar", state="normal")


class AppView(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controlador_usuario = ControladorUsuario()
        self.controlador_leds = ControladorLEDs()
        self.controlador_errores = ControladorErrores(self)

        self.hilo_ws = None
        self.loop = None
        self.ws_stop_event = None

        self.title("Led's up")
        self.iconbitmap(resource_path("imagenes/icono.ico"))
        self.geometry("600x400")
        self.resizable(False, False)

        self.statusLabel = ctk.CTkLabel(self, text="Estado:")
        self.statusLabel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.statusEntry = ctk.CTkEntry(self, state='disabled')
        self.statusEntry.grid(row=0, column=1, padx=10, pady=10)
        self.set_status_entry("Desconectado", "red")

        self.userLabel = ctk.CTkLabel(self, text="Usuario:")
        self.userLabel.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.userEntry = ctk.CTkEntry(self, state='disabled')
        self.userEntry.grid(row=1, column=1, padx=10, pady=10)

        self.set_user_entry(self.controlador_usuario.get_user_name())

        self.ConnectButton = ctk.CTkButton(self, text="Conectar", command=self.change_status)
        self.ConnectButton.grid(row=4, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.dispositivosFrame = DispositivosFrame(self)
        self.dispositivosFrame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.hilo_ws = None

    def set_user_entry(self, nombre):
        if not nombre:
            nombre = "Desconocido"

        self.userEntry.configure(state="normal")
        self.userEntry.insert(0, nombre)
        self.userEntry.configure(state="disabled")

    def set_status_entry(self, texto, color):
        self.statusEntry.configure(state="normal")
        self.statusEntry.delete(0, "end")
        self.statusEntry.insert(0, texto)
        self.statusEntry.configure(state="disabled", text_color=color)

    def change_status(self):
        self.ConnectButton.configure(state="disabled")

        if self.statusEntry.get() == "Desconectado":
            self.set_status_entry("Cargando...", "orange")

            self.ws_stop_event = asyncio.Event()
            self.loop = asyncio.new_event_loop()

            hilo_procesador = threading.Thread(target=procesar_comandos_thread, args=(self.controlador_leds, self),
                                               daemon=True)
            hilo_procesador.start()

            def iniciar_websocket():
                asyncio.set_event_loop(self.loop)
                self.loop.run_until_complete(escuchar_websocket(self, self.ws_stop_event))

            self.hilo_ws = threading.Thread(target=iniciar_websocket, daemon=True)
            self.hilo_ws.start()

        else:
            self.set_status_entry("Desconectado", "red")
            self.ConnectButton.configure(text="Conectar")
            detener_theads_viejos()

            if self.ws_stop_event:
                self.loop.call_soon_threadsafe(self.ws_stop_event.set)

            self.ConnectButton.configure(state="normal")

    def reportar_error(self, detalle, contexto):
        self.controlador_errores.enviar_error(modelo_error=ModeloError(detalle, contexto))


class DispositivosFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.labels = []

    def actualizar_dispositivos(self, dispositivos):
        for label in self.labels:
            label.destroy()
        self.labels.clear()

        for idx, (nombre_dispositivo, accion) in enumerate(dispositivos.items()):
            label = ctk.CTkLabel(self, text=f"Dispositivo: {nombre_dispositivo} -> {accion}")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            self.labels.append(label)
