from app.bot.notify import send_message

def handle_command(chat_id, text):
    if text.startswith("/start"):
        send_message(chat_id, "👋 ¡Bienvenido al bot Baywatchers!")
    elif text.startswith("/ayuda"):
        send_message(chat_id, "📌 Comandos:\n/start\n/ayuda\n/vigilar <URL>\n/detener <URL>")
    elif text.startswith("/vigilar"):
        send_message(chat_id, "✅ Producto añadido (ficticio por ahora).")
    elif text.startswith("/detener"):
        send_message(chat_id, "❌ Producto eliminado (ficticio por ahora).")
    else:
        send_message(chat_id, "❓ Comando no reconocido.")
