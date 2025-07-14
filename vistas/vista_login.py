import base64
import hashlib
import os
import random
import secrets
import threading
import traceback
import webbrowser

import customtkinter as ctk
from PIL import Image, ImageSequence
from dotenv import load_dotenv

from auth_token.oauth_callback_server import run_server
from auth_token.oauth_token_server import TokenManager
from globales import resource_path
from vistas.vista_popup_mensaje import PopupMensaje

load_dotenv()


def generate_code_verifier(length=128):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"
    return ''.join(secrets.choice(allowed) for _ in range(length))


def calculate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
    return challenge


def authentication():
    code_verifier = generate_code_verifier(random.randint(43, 128))
    code_challenge = calculate_code_challenge(code_verifier)
    auth_url = os.environ.get('AUTH_URL')
    client_id = os.environ.get('CLIENT_ID')
    auth_url = auth_url.replace("{CLIENT_ID}", client_id)
    auth_url = auth_url.replace("{CODE_CHALLENGE}", code_challenge)
    webbrowser.open(auth_url)

    auth_code = run_server()

    try:
        TokenManager.get_token_with_code(auth_code, code_verifier)
    except Exception as e:
        raise Exception("Error al autentificar", e)


class Login(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Server LEDS UP")
        self.iconbitmap(resource_path("imagenes/icono.ico"))
        self.geometry("300x300")
        self.resizable(False, False)

        self.custom_font = ctk.CTkFont(family="Segoe UI", size=12)
        self.title_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")

        # Logo
        logo_img = Image.open(resource_path("imagenes/logo.png")).resize((160, 60), Image.Resampling.LANCZOS)
        logo = ctk.CTkImage(logo_img, size=(160, 60))
        logo_label = ctk.CTkLabel(self, image=logo, text="")
        logo_label.pack(pady=(24, 8))

        ctk.CTkLabel(self, text="¡Bienvenido!", font=self.title_font).pack()
        ctk.CTkLabel(self, text="Inicia sesión para usar la aplicación", font=self.custom_font).pack(pady=(0, 16))

        self.login_btn = ctk.CTkButton(self, text="AUTENTICACIÓN WEB", command=self.run_with_wait_window)
        self.login_btn.pack(pady=(0, 24))

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def run_with_wait_window(self):
        self.withdraw()
        ventana = VentanaEspera(self)

        def thread_func():
            try:
                authentication()

            except Exception as e:
                print("Error al autenticar", e)
                traceback.print_exc()
                popup = PopupMensaje(ventana, "Error al autenticar, vuelva a intentarlo más tarde", True)
                self.wait_window(popup)

            ventana.after(0, ventana.destroy)
            self.after(0, self.destroy)

        thread = threading.Thread(target=thread_func, daemon=True)
        thread.start()

        ventana.grab_set()

    def cerrar(self):
        self.destroy()


class VentanaEspera(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Server LEDS UP")
        self.iconbitmap(resource_path("imagenes/icono.ico"))
        self.geometry("250x220")
        self.resizable(False, False)

        self.custom_font = ctk.CTkFont(family="Segoe UI", size=9)
        self.title_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        ctk.CTkLabel(self, text="Esperando autenticación...", font=self.title_font).pack()

        self.label = ctk.CTkLabel(self, text="")
        self.label.pack(padx=10, pady=10)
        self.frames = []
        self.indice = 0

        self.cargar_gif(resource_path("imagenes/LedLogin.gif"))
        self.reproducir()

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def cargar_gif(self, ruta_gif):
        img = Image.open(ruta_gif)
        size = img.size
        self.frames = [
            ctk.CTkImage(frame.copy().convert("RGBA"), size=size)
            for frame in ImageSequence.Iterator(img)
        ]

    def reproducir(self):
        if self.frames:
            self.label.configure(image=self.frames[self.indice])
            self.indice = (self.indice + 1) % len(self.frames)
            self.after(60, self.reproducir)

    def cerrar(self):
        self.destroy()
