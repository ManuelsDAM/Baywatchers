from telegram.ext import ApplicationBuilder, CommandHandler
from app.bot.handlers import (
    start_command, ayuda_command, vigilar_command,
    detener_command, misproductos_command, checkinterval_command,
)
from app.config import BOT_TOKEN
from app.scheduler import start_scheduler
from app.bot.handlers.estadisticas import estadisticas_command

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    start_scheduler()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("ayuda", ayuda_command))
    app.add_handler(CommandHandler("vigilar", vigilar_command,block=False))
    app.add_handler(CommandHandler("detener", detener_command,block=False))
    app.add_handler(CommandHandler("misproductos", misproductos_command,block=False))
    app.add_handler(CommandHandler("checkinterval", checkinterval_command,block=False))
    app.add_handler(CommandHandler("estadisticas", estadisticas_command, block=False))

    print("Bot iniciado correctamente")
    app.run_polling()


if __name__ == "__main__":
    main()
