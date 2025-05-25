from app.bot.telegrambot import main_loop

if __name__ == "__main__":
    main_loop()


"""import request as req

from telegram.ext import Updater
from config.auth import token
if __name__ == '__main__':
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
Url = 'https://api.telegram.org/bot'
Key = ''"""