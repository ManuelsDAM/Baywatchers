from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, add_product_for_user
from app.scraper import extract_slug_from_url, get_product_data_from_api

async def vigilar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("⚠️ Usa el comando así: /vigilar <url>")
        return

    url = context.args[0]
    telegram_id = update.effective_user.id

    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id)

        try:
            slug = extract_slug_from_url(url)
            product_data = get_product_data_from_api(slug)
        except Exception as e:
            await update.message.reply_text(f"❌ Error al obtener datos del producto: {e}")
            return

        product = add_product_for_user(db, user, url, product_data["price"])
        await update.message.reply_text(
            f"✅ Vigilando producto: {product_data['name']}\nPrecio actual: {product_data['price']} €"
        )
    finally:
        db.close()
