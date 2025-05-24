import tkinter as tk
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageSequence # Necesitas Pillow
import os



# Simulamos credenciales válidas
USUARIO_VALIDO = "juan"
PASSWORD_VALIDO = "1234"

class ModernLogin(tk.Tk):
    def __init__(self):
        super().__init__()
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

        # Bienvenida
        tk.Label(self, text="¡Bienvenido!", font=self.title_font, bg="#f5f8fa", fg="#222").pack()
        tk.Label(self, text="Inicia sesión para usar la aplicación", font=self.custom_font, bg="#f5f8fa", fg="#555").pack(pady=(0, 16))

        # Botón moderno
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
            command=self.web_auth
        )
        self.login_btn.pack(pady=(0, 24))

        # Efecto hover
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#198fd9"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#1da1f2"))

    def web_auth(self):
        self.withdraw()  # Oculta la ventana principal

        auth_url = os.environ.get("AUTH_URL")
        webbrowser.open(auth_url)

        CallbackHandler.do_GET()

        ventana = VentanaEspera()
        ventana.mainloop()

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
            self.after(60, self.reproducir)  # Ajusta el tiempo si va muy rápido/lento

    def cerrar(self):
        self.destroy()
        self.master.destroy()  # Cierra el root principal también


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extrae el código de la URL
        # Intercambia el código por el token
        pass

httpd = HTTPServer(('localhost', 12345), CallbackHandler)
httpd.handle_request()
