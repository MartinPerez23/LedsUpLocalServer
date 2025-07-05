import customtkinter as ctk

class PopupMensaje(ctk.CTkToplevel):
    def __init__(self, parent, mensaje, is_error):
        super().__init__(parent if parent else None)
        if is_error:
            self.title("Error")
        else:
            self.title("Info")

        self.iconbitmap(resource_path("imagenes/icono.ico"))
        self.resizable(False, False)

        if parent:
            self.transient(parent)
        self.grab_set()
        self.lift()
        self.attributes("-topmost", True)

        try:
            from PIL import Image
            if is_error:
                img = ctk.CTkImage(Image.open("imagenes/error.png"), size=(32, 32))
            else:
                img = ctk.CTkImage(Image.open("imagenes/informacion.png"), size=(32, 32))
            icono = ctk.CTkLabel(self, image=img, text="")
            icono.pack(pady=(10, 0))
        except Exception:
            pass

        label = ctk.CTkLabel(self, text=mensaje, wraplength=250, justify="center")
        label.pack(pady=10, padx=10)

        if is_error:
            boton = ctk.CTkButton(self, text="Aceptar", command=self.destroy, fg_color="red", hover_color="#1F6AA5")
        else:
            boton = ctk.CTkButton(self, text="Aceptar", command=self.destroy, fg_color="#1F6AA5")

        boton.pack(pady=10)

        self.update_idletasks()
        width = self.winfo_reqwidth() + 20
        height = self.winfo_reqheight() + 20

        if parent:
            parent.update_idletasks()
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()

            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
        else:
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")