from app.bot.notify import send_message
from telegram import Update
from telegram.ext import ContextTypes

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Bienvenido al bot Baywatchers!")

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 Comandos:\n/start\n/ayuda\n/vigilar <URL>\n/detener <URL>")

async def handle_vigilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Producto añadido (ficticio por ahora).")

async def handle_detener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Producto eliminado (ficticio por ahora).")
