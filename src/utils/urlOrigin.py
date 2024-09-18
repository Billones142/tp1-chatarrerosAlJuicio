from urllib.parse import urlparse

def get_origin(url):
    parsed_url = urlparse(url)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return origin

def get_main_origin(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')
    
    # Detectar dominios que tienen más de dos niveles (como .com.ar, .co.uk, etc.)
    if len(domain_parts) > 2 and domain_parts[-2] in ["com", "co", "org"]:
        main_domain = ".".join(domain_parts[-3:])  # Unir los últimos tres componentes
    else:
        main_domain = ".".join(domain_parts[-2:])  # Unir los últimos dos componentes
    
    # Crear la URL con el esquema y el dominio principal
    origin = f"{parsed_url.scheme}://{main_domain}"
    
    return origin