from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, list_user_products

async def misproductos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id)
        products = list_user_products(db, user)
        if not products:
            await update.message.reply_text("No tienes productos vigilados.")
            return
        
        message = "🛒 Productos que vigilas:\n" + "\n".join([f"- {p.url}" for p in products])
        await update.message.reply_text(message)
    finally:
        db.close()
