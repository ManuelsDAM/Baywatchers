# app/bot/handlers/detener.py
from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, remove_product_for_user

async def detener_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usa el comando así: /detener <url>")
        return

    url = context.args[0]
    telegram_id = update.effective_user.id

    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id)
        removed = remove_product_for_user(db, user, url)
        if removed:
            await update.message.reply_text(f"❌ Dejaste de vigilar el producto:\n{url}")
        else:
            await update.message.reply_text("⚠️ No estabas vigilando ese producto.")
    finally:
        db.close()
