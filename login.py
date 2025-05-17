import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Simulamos credenciales válidas
USUARIO_VALIDO = "juan"
PASSWORD_VALIDO = "1234"

def iniciar_login():
    usuario = entry_usuario.get()
    password = entry_password.get()

    if not usuario or not password:
        messagebox.showerror("Error", "Completa usuario y contraseña")
        return

    if usuario == USUARIO_VALIDO and password == PASSWORD_VALIDO:
        messagebox.showinfo("Éxito", "¡Login exitoso!")
        root.destroy()  # Cierra la ventana de login
        # Desde tu archivo principal, acá podés continuar con lo que quieras
    else:
        messagebox.showerror("Login fallido", "Usuario o contraseña incorrectos")

# ---------- Interfaz gráfica ----------
root = tk.Tk()
root.title("Server LEDS UP")
root.geometry("350x300")

# Cargar imagen (ajustá el path si hace falta)
logo_img = Image.open("imagenes/logo.png")
logo_img = logo_img.resize((160, 80), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)

# Mostrar imagen
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=20)

tk.Label(root, text="Usuario").pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Contraseña").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Iniciar sesión", command=iniciar_login).pack(pady=10)

root.mainloop()