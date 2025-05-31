from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Bienvenido a Baywatchers! Usa /vigilar <URL> para empezar a vigilar productos.\n"
        "Usa /ayuda para ver los comandos disponibles."
    )

async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *Comandos disponibles:*\n\n"
        "▶️ /start - Inicia el bot y da la bienvenida\n"
        "🆘 /ayuda - Muestra esta lista de comandos\n"
        "👟 /vigilar <url> - Empieza a vigilar un producto\n"
        "❌ /detener <url> - Deja de vigilar un producto\n"
        "📋 /misproductos - Muestra los productos que estás vigilando\n"
        "⏱ /checkinterval <minutos> - Cambia la frecuencia de revisión\n"
        "📊 /estadisticas <url> - Muestra media, máximo, mínimo y últimos 10 precios"
    )