import customtkinter as ctk
from PIL import Image, ImageTk

# Configuración básica
ctk.set_appearance_mode("Dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema azul

# Crear ventana principal
root = ctk.CTk()
root.geometry("800x600")
root.title("Catálogo de Productos Scrapeados")

# Función para mostrar productos
def mostrar_producto(nombre, precio, imagen_ruta):
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=10, padx=10, fill="x")
    
    # Cargar imagen del producto
    img = Image.open(imagen_ruta)
    img = img.resize((100, 100))
    img_tk = ImageTk.PhotoImage(img)
    
    img_label = ctk.CTkLabel(master=frame, image=img_tk, text="")
    img_label.image = img_tk
    img_label.pack(side="left", padx=10)   
    
    # Mostrar nombre y precio
    nombre_label = ctk.CTkLabel(master=frame, text=nombre)
    nombre_label.pack(side="top", padx=10)
    
    precio_label = ctk.CTkLabel(master=frame, text=f"${precio}")
    precio_label.pack(side="bottom", padx=10)

# Ejemplo de productos scrapeados
productos = [
    {"nombre": "Taladro XYZ", "precio": "5000", "imagen": "ruta_imagen1.jpg"},
    {"nombre": "Sierra Eléctrica ABC", "precio": "7000", "imagen": "ruta_imagen2.jpg"},
]

# Mostrar cada producto
for producto in productos:
    mostrar_producto(producto["nombre"], producto["precio"], producto["imagen"])

root.mainloop()
