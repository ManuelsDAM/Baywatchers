DATABASE_URL = "sqlite:///./baywatchers.db"
from app.db.models import Product, PriceHistory
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def insertar_nuevo_precio(session, product_id: int, nuevo_precio: float):
    # Buscar el producto por id
    producto = session.query(Product).filter_by(id=product_id).first()
    if not producto:
        raise ValueError(f"Producto con id {product_id} no encontrado.")

    # Crear un nuevo registro de historial de precios
    nuevo_historial = PriceHistory(
        product_id=product_id,
        price=nuevo_precio,
        timestamp=datetime.now(timezone.utc)
    )
    session.add(nuevo_historial)

    # Actualizar el último precio del producto
    producto.last_price = nuevo_precio

    # Guardar los cambios
    session.commit()

# Ejemplo de uso:
#Base.metadata.create_all(bind=engine)
insertar_nuevo_precio(session, 3, 69)