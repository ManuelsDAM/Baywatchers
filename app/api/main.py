from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db import SessionLocal
from app.db.models import User, Product, PriceHistory
from app.db.crud import get_or_create_user, add_product_for_user, remove_product_for_user
from app.scraper import extract_slug_from_url, get_product_data_from_api

app = FastAPI()

# Modelo para añadir productos desde la API
class ProductInput(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "API Baywatchers funcionando"}

@app.get("/users/{telegram_id}")
def get_user_config(telegram_id: int):
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "telegram_id": user.telegram_id,
        "products": len(user.products)
    }

@app.get("/products/{telegram_id}")
def get_user_products(telegram_id: int):
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    products = [
        {"id": p.id, "url": p.url, "last_price": p.last_price, "size": p.size}
        for p in user.products
    ]
    db.close()
    return products

@app.post("/products/{telegram_id}")
def add_product(telegram_id: int, item: ProductInput):
    db = SessionLocal()
    user = get_or_create_user(db, telegram_id)

    try:
        slug = extract_slug_from_url(item.url)
        data = get_product_data_from_api(slug)
    except Exception:
        db.close()
        raise HTTPException(status_code=400, detail="No se pudo obtener el producto desde la API")

    product = add_product_for_user(
        db=db,
        user=user,
        url=item.url,
        last_price=data["price"]
    )
    db.close()
    return {
        "message": "Producto añadido con éxito",
        "product": {
            "id": product.id,
            "url": product.url,
            "last_price": product.last_price
        }
    }

@app.delete("/products/{telegram_id}")
def delete_product(telegram_id: int, item: ProductInput):
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    success = remove_product_for_user(db, user, item.url)
    db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado"}
