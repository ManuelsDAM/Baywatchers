from app.bot.telegrambot import main
from app.bot.notify import send_message
from decouple import config
from app.db import engine
from app.db.models import Base
from app.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    chat_id = int(config("CHAT_ID"))
    send_message(chat_id,"🔔 Prueba de notificación automática.")
    main()
    start_scheduler()

"""import request as req

from telegram.ext import Updater
from config.auth import token
if __name__ == '__main__':
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
Url = 'https://api.telegram.org/bot'
Key = ''"""