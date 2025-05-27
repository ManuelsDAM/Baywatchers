from bs4 import BeautifulSoup
import requests
from app.db import SessionLocal
from app.db.models import ProductHistory

def extract_product_info_from_url(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0"  # Evita bloqueos
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else "Título no encontrado"
    current_price_span = soup.find("span", class_="customer-price")
    original_price_span = soup.find("span", class_="product-discount-price")

    # Limpieza
    def parse_price(span):
        if not span:
            return None
        return float(span.get_text(strip=True).replace("€", "").replace(",", ".").strip())

    current_price = parse_price(current_price_span)
    original_price = parse_price(original_price_span)
    descuento_activo = "Sí" if original_price else "No"

    return {
        "title": title,
        "price": current_price,
        "original_price": original_price,
        "descuento_activo": descuento_activo
    }

def track_product(url: str):
    data = extract_product_info_from_url(url)
    db = SessionLocal()
    record = ProductHistory(
        url=url,
        title=data["title"],
        price=data["price"],
        original_price=data["original_price"],
        descuento_activo=data["descuento_activo"]
    )
    db.add(record)
    db.commit()
    db.close()
    print(f"[{data['title']}] Precio registrado: {data['price']}€")
