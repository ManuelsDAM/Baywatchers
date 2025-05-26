from telegram.ext import ApplicationBuilder, CommandHandler
from app.bot.commands import handle_start, handle_help, handle_vigilar, handle_detener
from app.config import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("ayuda", handle_help))
    app.add_handler(CommandHandler("vigilar", handle_vigilar))
    app.add_handler(CommandHandler("detener", handle_detener))

    print("Bot iniciado correctamente")
    app.run_polling()
