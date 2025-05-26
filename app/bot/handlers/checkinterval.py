from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, update_check_interval_for_user

async def checkinterval_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Usa el comando así: /checkinterval <minutos> (debe ser un número entero).")
        return
    
    interval = int(context.args[0])
    if interval < 1 or interval > 1440:
        await update.message.reply_text("⚠️ El intervalo debe estar entre 1 y 1440 minutos (24 horas).")
        return

    telegram_id = update.effective_user.id
    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id)
        updated_count = update_check_interval_for_user(db, user, interval)
        if updated_count > 0:
            await update.message.reply_text(f"✅ Intervalo de revisión actualizado a {interval} minutos para {updated_count} producto(s).")
        else:
            await update.message.reply_text("⚠️ No tienes productos vigilados para actualizar.")
    finally:
        db.close()