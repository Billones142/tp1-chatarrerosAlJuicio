import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

# Crear la ventana principal
root = ctk.CTk()
root.title("Buscador de Productos")
root.geometry("800x600")

# Función para realizar el scraping (por ahora es un ejemplo que tú conectarás con los actores)
def buscar_producto(producto):
    # Aquí conectas con tus actores y devuelves los productos scrappeados
    # Esto es solo un ejemplo, tú aquí integrarás la lógica de tus actores
    productos_scrappeados = [
        {"nombre": "Taladro Inalámbrico", "precio": "$1999", "imagen": "taladro.jpg"},
        {"nombre": "Destornillador", "precio": "$499", "imagen": "destornillador.jpg"}
    ]
    return productos_scrappeados

# Función para mostrar los productos obtenidos después del scraping
def mostrar_productos(productos):
    # Limpiar la ventana para mostrar los productos
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un frame para los productos
    frame_productos = ctk.CTkFrame(master=root, corner_radius=10)
    frame_productos.pack(pady=20, padx=20, fill="both", expand=True)

    # Mostrar cada producto en un frame
    for producto in productos:
        frame = ctk.CTkFrame(master=frame_productos, corner_radius=10)
        frame.pack(pady=10, padx=10, fill="x")
        
        # Cargar y mostrar imagen
        img = Image.open(producto['imagen'])
        img = img.resize((100, 100), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        
        img_label = ctk.CTkLabel(master=frame, image=img_tk)
        img_label.image = img_tk
        img_label.pack(side="left", padx=10)
        
        # Mostrar nombre y precio
        name_label = ctk.CTkLabel(master=frame, text=f"Nombre: {producto['nombre']}", font=("Arial", 16))
        name_label.pack(anchor="w", pady=5)
        
        price_label = ctk.CTkLabel(master=frame, text=f"Precio: {producto['precio']}", font=("Arial", 14))
        price_label.pack(anchor="w", pady=5)

    # Botón para realizar una nueva búsqueda
    btn_nueva_busqueda = ctk.CTkButton(master=frame_productos, text="Nueva Búsqueda", command=nueva_busqueda)
    btn_nueva_busqueda.pack(pady=20)

# Función que se llama al hacer clic en el botón de búsqueda
def buscar_y_mostrar():
    producto = entry_producto.get()
    if producto:
        # Llamar a la función de scraping (donde tú conectarás los actores)
        productos = buscar_producto(producto)
        # Mostrar los productos
        mostrar_productos(productos)
    else:
        messagebox.showerror("Error", "Por favor, ingresa un nombre de producto")

# Función para volver a la pantalla de búsqueda
def nueva_busqueda():
    # Limpiar la ventana para la nueva búsqueda
    for widget in root.winfo_children():
        widget.destroy()
    mostrar_pantalla_busqueda()

# Función para mostrar la pantalla de búsqueda
def mostrar_pantalla_busqueda():
    # Crear un frame para la búsqueda
    frame_busqueda = ctk.CTkFrame(master=root, corner_radius=10)
    frame_busqueda.pack(pady=20, padx=20)

    # Etiqueta y cuadro de texto para el nombre del producto
    label_producto = ctk.CTkLabel(master=frame_busqueda, text="Ingrese el nombre del producto:", font=("Arial", 16))
    label_producto.pack(pady=10)

    global entry_producto
    entry_producto = ctk.CTkEntry(master=frame_busqueda, width=300)
    entry_producto.pack(pady=10)

    # Botón para buscar el producto
    btn_buscar = ctk.CTkButton(master=frame_busqueda, text="Buscar Producto", command=buscar_y_mostrar)
    btn_buscar.pack(pady=10)

# Mostrar la pantalla de búsqueda al iniciar la aplicación
mostrar_pantalla_busqueda()

# Ejecutar la interfaz
root.mainloop()
