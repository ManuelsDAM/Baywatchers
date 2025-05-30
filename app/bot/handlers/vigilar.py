from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, add_product_for_user
from app.scraper import extract_slug_from_url, get_product_data_from_api
from urllib.parse import urlparse
import re

async def vigilar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("⚠️ Usa el comando así: /vigilar <url>")
        return

    url = context.args[0]

    # Validación básica de URL
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http") or "fittestfreakest" not in parsed.netloc:
        await update.message.reply_text("⚠️ URL inválida. Debe ser de fittestfreakest.es")
        return

    slug = extract_slug_from_url(url)

    # Deducción de talla desde slug (si termina en número)
    slug_parts = slug.split("-")
    size = slug_parts[-1] if re.match(r"^[0-9]{2,3}$", slug_parts[-1]) else None

    try:
        data = get_product_data_from_api(slug)
    except ValueError:
        await update.message.reply_text("❌ No se encontró el producto en la API.")
        return

    db = SessionLocal()
    try:
        user = get_or_create_user(db, update.effective_user.id)
        product = add_product_for_user(
            db=db,
            user=user,
            url=url,
            last_price=data["price"],
            size=size
        )

        await update.message.reply_text(
            f"✅ Vigilando producto: *{data['name']}*"
            + (f"\n📏 Talla: {size}" if size else "")
            + f"\n💰 Precio actual: {data['price']} €",
            parse_mode="Markdown"
        )
    finally:
        db.close()
