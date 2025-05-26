from app.bot.telegrambot import main
from app.bot.notify import send_message
from decouple import config

if __name__ == "__main__":
    chat_id = int(config("CHAT_ID"))
    send_message(chat_id,"🔔 Prueba de notificación automática.")
    main()

"""import request as req

from telegram.ext import Updater
from config.auth import token
if __name__ == '__main__':
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
Url = 'https://api.telegram.org/bot'
Key = ''"""