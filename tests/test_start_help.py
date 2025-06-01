import pytest
from unittest.mock import AsyncMock, MagicMock
from app.bot.handlers.start_help import start_command, ayuda_command  

@pytest.mark.asyncio
async def test_start_command():
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_message

    context = MagicMock()

    await start_command(mock_update, context)

    mock_message.reply_text.assert_called_once()
    text = mock_message.reply_text.call_args[0][0]
    assert "👋 ¡Bienvenido a Baywatchers!" in text
    assert "/vigilar <URL>" in text
    
@pytest.mark.asyncio
async def test_ayuda_command():
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_message

    context = MagicMock()

    await ayuda_command(mock_update, context)

    mock_message.reply_text.assert_called_once()
    text = mock_message.reply_text.call_args[0][0]
    assert "📌 *Comandos disponibles:*" in text
    assert "/start" in text
    assert "/vigilar" in text
    assert "/detener" in text
    assert "/misproductos" in text
    assert "/checkinterval" in text
    assert "/estadisticas" in text