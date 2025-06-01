import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_send_message():
    chat_id = 1234
    text = "Mensaje de prueba"
    with patch("telegram.Bot.send_message", new_callable=AsyncMock) as mock_send_message:
        from app.bot.notify import send_message  # import inside to ensure patching
        await send_message(chat_id, text)
        mock_send_message.assert_awaited_once_with(chat_id=chat_id, text=text, parse_mode="Markdown")