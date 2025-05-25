from app.config import BOT_TOKEN
from app.bot.commands import handle_command
import requests
import time

URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    response = requests.get(f"{URL}/getUpdates", params=params)
    print(response.text)
    return response.json()

def main_loop():
    offset = None
    print("Bot iniciado")
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            handle_command(chat_id, text)

            offset = update["update_id"] + 1
        time.sleep(1)
