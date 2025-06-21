import base64
import hashlib
import os
import random
import secrets
import threading
import tkinter as tk
import webbrowser
from tkinter import font as tkfont

from PIL import Image, ImageTk, ImageSequence
from dotenv import load_dotenv

from auth_token.oauth_callback_server import run_server
from auth_token.oauth_token_server import TokenManager

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

    TokenManager.get_token_with_code(auth_code,code_verifier)


class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.code_verifier = None
        self.title("Server LEDS UP")
        self.geometry("350x320")
        self.configure(bg="#f5f8fa")
        self.resizable(False, False)

        self.custom_font = tkfont.Font(family="Segoe UI", size=12)
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")

        # Logo
        logo_img = Image.open("imagenes/logo.png")
        logo_img = logo_img.resize((160, 60), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(self, image=self.logo, bg="#f5f8fa")
        logo_label.pack(pady=(24, 8))

        tk.Label(self, text="¡Bienvenido!", font=self.title_font, bg="#f5f8fa", fg="#222").pack()
        tk.Label(self, text="Inicia sesión para usar la aplicación", font=self.custom_font, bg="#f5f8fa",
                 fg="#555").pack(pady=(0, 16))

        self.login_btn = tk.Button(
            self,
            text="AUTENTICACIÓN WEB",
            font=self.custom_font,
            bg="#1da1f2",
            fg="white",
            activebackground="#198fd9",
            activeforeground="white",
            bd=0,
            relief="flat",
            width=24,
            height=2,
            cursor="hand2",
            command=self.run_with_wait_window
        )
        self.login_btn.pack(pady=(0, 24))

        # Efecto hover
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#198fd9"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#1da1f2"))

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def run_with_wait_window(self):
        self.withdraw()
        ventana = VentanaEspera()

        def thread_func():
            authentication()
            ventana.after(0, ventana.quit)

        thread = threading.Thread(target=thread_func)
        thread.daemon = True
        thread.start()
        ventana.mainloop()
        ventana.destroy()

        self.destroy()

    def cerrar(self):
        self.destroy()
        self.master.destroy()


class VentanaEspera(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Server LEDS UP")
        self.geometry("250x220")
        self.configure(bg="#f5f8fa")
        self.resizable(False, False)

        self.custom_font = tkfont.Font(family="Segoe UI", size=9)
        self.title_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

        tk.Label(self, text="Esperando autenticación...", font=self.title_font, bg="#f5f8fa", fg="#222").pack()

        self.label = tk.Label(self, bg="#f5f8fa")
        self.label.pack(padx=10, pady=10)
        self.frames = []
        self.cargar_gif("imagenes/LedLogin.gif")
        self.indice = 0
        self.reproducir()

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def cargar_gif(self, ruta_gif):
        img = Image.open(ruta_gif)
        self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                       for frame in ImageSequence.Iterator(img)]

    def reproducir(self):
        frame_actual = self.frames[self.indice]
        self.label.config(image=frame_actual)
        self.indice = (self.indice + 1) % len(self.frames)
        self.after(60, self.reproducir)

    def cerrar(self):
        self.destroy()
        self.master.destroy()
