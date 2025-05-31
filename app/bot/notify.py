from telegram import Bot
from app.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

async def send_message(chat_id: int, text: str) -> None:
    await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
