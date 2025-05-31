from telegram import Update
from telegram.ext import ContextTypes
from app.db import SessionLocal
from app.db.crud import get_or_create_user, get_price_statistics, get_last_10_prices

async def estadisticas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("📌 Usa el comando así: /estadisticas <url>")
        return

    url = context.args[0]
    db = SessionLocal()
    try:
        user = get_or_create_user(db, update.effective_user.id)
        product = next((p for p in user.products if p.url == url), None)

        if not product:
            await update.message.reply_text("⚠️ No estás vigilando ese producto.")
            return

        avg, max_, min_ = get_price_statistics(db, product.id)
        last_prices = get_last_10_prices(db, product.id)

        texto = (f"📊 Estadísticas para:\n{product.url}\n\n"
                 f"🔹 Precio medio: {avg} €\n"
                 f"🔹 Máximo: {max_} €\n"
                 f"🔹 Mínimo: {min_} €\n\n"
                 f"📈 Últimos 10 precios:\n" +
                 "\n".join(f"{p.price} € ({p.timestamp.strftime('%d-%m-%Y %H:%M')})" for p in last_prices)
                 )

        await update.message.reply_text(texto)
    finally:
        db.close()
