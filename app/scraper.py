import requests
from urllib.parse import urlparse

def extract_slug_from_url(url: str) -> str:
    """
    Extrae el slug desde la URL completa de Fittest Freakest.
    Ej: https://www.fittestfreakest.es/zapatillas/while-on-earth-move-trainer
    Devuelve: while-on-earth-move-trainer
    """
    path = urlparse(url).path
    parts = path.strip("/").split("/")
    if parts and parts[-1]:
        return parts[-1]
    raise ValueError("No se pudo extraer el slug de la URL")

def get_product_data_from_api(slug: str) -> dict:
    """
    Llama a la API de Fittest Freakest y devuelve nombre y precio del producto.
    """
    url = f"https://api.fittestfreakest.es/catalog/zapatillas/{slug}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Producto no encontrado o error de API ({response.status_code})")

    data = response.json()

    return {
        "name": data.get("name", "Nombre desconocido"),
        "price": data.get("price", 0.0)
    }
