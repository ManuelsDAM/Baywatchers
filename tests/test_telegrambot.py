import pytest
from unittest.mock import patch, MagicMock

def test_main_inicializa_bot_y_handlers():
    with patch("app.bot.telegrambot.ApplicationBuilder") as mock_builder, \
         patch("app.bot.telegrambot.start_scheduler") as mock_scheduler:

        mock_app = MagicMock()
        mock_builder.return_value.token.return_value.build.return_value = mock_app

        from app.bot import telegrambot
        telegrambot.main()

        # Verifica que se llama a ApplicationBuilder y se construye el bot
        mock_builder.assert_called_once()
        mock_builder.return_value.token.assert_called_once()
        mock_builder.return_value.token.return_value.build.assert_called_once()

        # Verifica que se llama a start_scheduler
        mock_scheduler.assert_called_once()

        # Verifica que se añaden los handlers
        assert mock_app.add_handler.call_count == 7

        # Verifica que se llama a run_polling
        mock_app.run_polling.assert_called_once()