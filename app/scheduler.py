from apscheduler.schedulers.background import BackgroundScheduler
from app.db import SessionLocal
from app.db.models import Product, User, PriceHistory
from app.scraper import extract_slug_from_url, get_product_data_from_api
from app.bot.notify import send_message
import asyncio

scheduler = BackgroundScheduler()

def track_product(product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter_by(id=product_id).first()
        if not product:
            return

        slug = extract_slug_from_url(product.url)
        data = get_product_data_from_api(slug)
        new_price = data["price"]

        if product.last_price != new_price:
            print("🎯 Cambio detectado")
            user = db.query(User).filter_by(id=product.user_id).first()
            if user:
                asyncio.run(send_message(
                    chat_id=user.telegram_id,
                    text=(f"💸 El precio de *{data['name']}* ha cambiado:\n"
                          f"Antes: {product.last_price} €\nAhora: {new_price} €")
                ))

            # Actualizar precio
            product.last_price = new_price

            # Guardar en historial
            nuevo_registro = PriceHistory(
                product_id=product.id,
                price=new_price
            )
            db.add(nuevo_registro)

            db.commit()

        print(f"🔁 Revisado: {product.url} ({product.id})")

    except Exception as e:
        print(f"❌ Error al revisar producto {product_id}: {e}")
    finally:
        db.close()

def reprogram_all_jobs():
    db = SessionLocal()
    try:
        scheduler.remove_all_jobs()
        productos = db.query(Product).all()
        for p in productos:
            print(f"⏱️ Programando producto: {p.url} cada {p.check_interval} minutos")
            scheduler.add_job(
                func=lambda pid=p.id: track_product(pid),
                trigger="interval",
                minutes=p.check_interval,
                id=str(p.id),
                replace_existing=True
            )
    finally:
        db.close()

def start_scheduler():
    reprogram_all_jobs()
    scheduler.add_job(reprogram_all_jobs, trigger="interval", minutes=10)
    scheduler.start()
    print("🔄 Scheduler en marcha...")
