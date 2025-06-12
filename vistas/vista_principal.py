import asyncio
import json
import os
import queue
import threading

import customtkinter as ctk
import requests
import websockets

import globales
from controladores.controlador_leds import ControladorLEDs

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

appWidth, appHeight = 600, 400

comando_queue = queue.Queue()


async def escuchar_websocket(app_view, stop_event: asyncio.Event):
    header = [
        ("Origin", os.environ.get('ORIGIN')),
        ("Authorization", f"Bearer {globales.AUTH_TOKEN_USUARIO}")
    ]
    try:
        async with websockets.connect(os.environ.get('WS_URI'), extra_headers=header) as websocket:
            while not stop_event.is_set():
                try:
                    mensaje = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(mensaje)
                    comando = data.get('data')

                    if comando:
                        comando_queue.put(comando)
                        await websocket.send(json.dumps({"estado": "ok"}))
                    else:
                        PopupMensaje(app_view, "Se recibio un comando inesperado desde la web, vuelva a intentarlo")
                        app_view.enviar_error_a_la_web("Formato inesperado:" + str(data),
                                                       'Al recibir el comando desde la web')

                except asyncio.TimeoutError:
                    # Este timeout permite verificar periódicamente si stop_event está seteado
                    continue

    except Exception as e:
        app_view.enviar_error_a_la_web('Al recibir el comando desde la web', str(e))
        app_view.ConnectButton._clicked()
    finally:
        await websocket.close()


def procesar_comandos_thread(controlador: ControladorLEDs, app_view):
    while True:
        comando = comando_queue.get()
        if comando is None:
            break
        controlador.procesar_comando(comando, app_view)


class AppView(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hilo_ws = None
        self.loop = None
        self.ws_stop_event = None

        self.title("Led's up")
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
        self.set_user_entry(globales.NOMBRE_USUARIO)

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
        if self.statusEntry.get() == "Desconectado":
            self.set_status_entry("Conectado", "green")
            self.ConnectButton.configure(text="Desconectar")

            # Acá inicializamos el event y el loop
            self.ws_stop_event = asyncio.Event()
            self.loop = asyncio.new_event_loop()

            controlador = ControladorLEDs()
            hilo_procesador = threading.Thread(target=procesar_comandos_thread, args=(controlador, self), daemon=True)
            hilo_procesador.start()

            # Defino la función para correr el websocket con el loop que creamos
            def iniciar_websocket():
                asyncio.set_event_loop(self.loop)  # seteamos el loop en el thread
                self.loop.run_until_complete(escuchar_websocket(self, self.ws_stop_event))

            self.hilo_ws = threading.Thread(target=iniciar_websocket, daemon=True)
            self.hilo_ws.start()

        else:
            self.set_status_entry("Desconectado", "red")
            self.ConnectButton.configure(text="Conectar")

            # Al desconectar, seteo el event para que termine la corutina
            if self.ws_stop_event:
                self.loop.call_soon_threadsafe(self.ws_stop_event.set)  # thread safe para setear el event

    def enviar_error_a_la_web(self, detalle, contexto):

        if not globales.AUTH_TOKEN_USUARIO:
            PopupMensaje(self, 'No se puede enviar el error, no hay usuario autenticado. Intente ingregar nuevamente')
            return

        error_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + globales.AUTH_TOKEN_USUARIO
        }

        error_data = {
            'detalle': detalle,
            'contexto': contexto,
            'origen': 'app'
        }

        response = requests.post(os.environ.get('ERROR_URL'), json=error_data, headers=error_headers, verify=False)

        if response.status_code == 201:
            PopupMensaje(self, 'Error reportado, espera a ser contactado por el equipo de soporte')
        else:
            PopupMensaje(self, 'No se ha podido enviar el error, por favor contacte via web')


class DispositivosFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.labels = []

    def actualizar_dispositivos(self, dispositivos):
        for label in self.labels:
            label.destroy()
        self.labels.clear()

        for idx, (nombre_dispositivo, accion) in enumerate(dispositivos.items()):
            label = ctk.CTkLabel(self, text=f"Nombre {nombre_dispositivo} -> {accion}")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            self.labels.append(label)


class PopupMensaje(ctk.CTkToplevel):
    def __init__(self, parent, mensaje):
        super().__init__(parent)
        self.title("Error")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.lift()
        self.attributes("-topmost", True)

        try:
            from PIL import Image
            error_img = ctk.CTkImage(Image.open("imagenes/error.png"), size=(32, 32))
            icono = ctk.CTkLabel(self, image=error_img, text="")
            icono.pack(pady=(10, 0))
        except Exception as e:
            print(e)
            pass

        label = ctk.CTkLabel(self, text=mensaje, wraplength=250, justify="center")
        label.pack(pady=10, padx=10)
        boton = ctk.CTkButton(self, text="Aceptar", command=self.destroy, fg_color="red", hover_color="#1F6AA5")
        boton.pack(pady=10)

        self.update_idletasks()
        width = self.winfo_reqwidth() + 20
        height = self.winfo_reqheight() + 20

        parent.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")
