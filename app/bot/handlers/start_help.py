from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Bienvenido a Baywatchers! Usa /vigilar <URL> para empezar a vigilar productos.\n"
        "Usa /ayuda para ver los comandos disponibles."
    )

async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos disponibles:\n"
        "/start - Inicio y bienvenida\n"
        "/ayuda - Mostrar esta ayuda\n"
        "/vigilar <URL> - Añadir producto\n"
        "/detener <URL> - Dejar de vigilar producto\n"
        "/misproductos - Ver tus productos vigilados\n"
        "/checkinterval <minutos> - Configurar intervalo de revisión"
    )