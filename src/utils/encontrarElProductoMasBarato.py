def limpiar_precio(string):
    # Convertimos a string en caso de que sea un número
    string = str(string)
    
    # Eliminamos símbolos de moneda y espacios en blanco
    string = string.replace('$', '').strip()
    
    # Mantenemos solo los caracteres numéricos, puntos y comas
    numero = ''.join([char for char in string if char.isdigit() or char in ['.', ',']])
    
    return numero


def limpiar_diccionario_productos(productos):
    """
    Elimina productos que contengan 'caja-vacia' en el link.
    
    :param productos: Lista de diccionarios con información de productos.
    :return: Lista filtrada sin productos de cajas vacías.
    """
    return [producto for producto in productos if 'caja-vacia' not in producto['link'].lower()]

def encontrar_producto_mas_barato(productos):
    """
    Encuentra el producto más barato en una lista de productos, después de eliminar los que contienen 'caja vacía'.

    :param productos: Lista de diccionarios, donde cada diccionario tiene la forma
    {'price': precio del producto, 'link': enlace del producto}.
    :return: Diccionario del producto más barato.
    """
    # Limpiar productos que son cajas vacías
    productos_filtrados = limpiar_diccionario_productos(productos)
    
    if not productos_filtrados:
        return (None, None)
    
    # Suponemos que el primer producto es el más barato al principio
    producto_mas_barato = productos_filtrados[0]
    precio_mas_barato = producto_mas_barato['price']
    
    # Iteramos sobre los productos restantes para encontrar el más barato
    for producto in productos_filtrados[1:]:
        precio_actual = producto['price']
        if precio_actual < precio_mas_barato:
            producto_mas_barato = producto
            precio_mas_barato = precio_actual
    
    return limpiar_precio(producto_mas_barato['price']), producto_mas_barato['link']

def comparar_precios_enlaces(lista_productos_por_enlace):
    """
    Compara los precios más bajos entre varios enlaces y retorna el más barato.

    :param lista_productos_por_enlace: Lista de listas, donde cada sublista contiene diccionarios de productos de un enlace.
    :return: Diccionario con el enlace del producto más barato entre todos los enlaces.
    """
    productos_mas_baratos = []

    # Obtener el producto más barato de cada enlace
    for productos in lista_productos_por_enlace:
        precio, link = encontrar_producto_mas_barato(productos)
        if precio is not None:
            productos_mas_baratos.append({'precio': precio, 'link': link})
    if not productos_mas_baratos:
        return "No se encontraron productos disponibles en los enlaces proporcionados."
    
    # Encontrar el producto más barato entre todos los enlaces
    producto_mas_barato = min(productos_mas_baratos, key=lambda x: x['precio'])
    
    return producto_mas_barato