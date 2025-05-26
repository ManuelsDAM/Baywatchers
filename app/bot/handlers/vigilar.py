from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, add_product_for_user

async def vigilar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("⚠️ Usa el comando así: /vigilar <url>")
        return

    url = context.args[0]
    telegram_id = update.effective_user.id

    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id)
        product = add_product_for_user(db, user, url)
        await update.message.reply_text(f"✅ Vigilando producto:\n{product.url}")
    finally:
        db.close()
