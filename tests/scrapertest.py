from bs4 import BeautifulSoup
import requests
from app.db import SessionLocal
from app.db.models import Product, PriceHistory
from datetime import datetime

def track_product(product_id: int):
    # 1. Abrir la base de datos
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        print(f"Producto con ID {product_id} no encontrado.")
        db.close()
        return

    try:
        # 2. Descargar la página del producto
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(product.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # 3. Extraer título
        title = soup.title.string.strip() if soup.title else "Sin título"

        # 4. Extraer precio actual y original
        def parse_price(selector):
            tag = soup.find("span", class_=selector)
            if tag:
                return float(tag.get_text(strip=True).replace("€", "").replace(",", "."))
            return None

        price = parse_price("customer-price")
        original_price = parse_price("product-discount-price")
        descuento_activo = "Sí" if original_price else "No"

        # 5. Guardar el histórico
        historial = PriceHistory(
            product_id=product.id,
            timestamp=datetime.utcnow(),
            price=price,
            original_price=original_price,
            descuento_activo=descuento_activo
        )
        db.add(historial)

        # 6. Actualizar el último precio en la tabla productos
        product.last_price = price

        db.commit()
        print(f"[{title}] Precio guardado: {price}€")

    except Exception as e:
        print(f"❌ Error rastreando producto {product.url}: {e}")
    finally:
        db.close()
