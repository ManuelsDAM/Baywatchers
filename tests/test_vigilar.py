import pytest
from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace

from app.bot.handlers.vigilar import vigilar_command

@pytest.mark.asyncio
async def test_vigilar_command_sin_argumentos():
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()
    mock_update = MagicMock()
    mock_update.message = mock_message
    context = SimpleNamespace(args=[])
    await vigilar_command(mock_update, context)
    mock_message.reply_text.assert_awaited_once_with("⚠️ Usa el comando así: /vigilar <url>")

@pytest.mark.asyncio
async def test_vigilar_command_url_invalida():
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()
    mock_update = MagicMock()
    mock_update.message = mock_message
    context = SimpleNamespace(args=["https://google.com/producto"])
    await vigilar_command(mock_update, context)
    mock_message.reply_text.assert_awaited_once_with("⚠️ URL inválida. Debe ser de fittestfreakest.es")

@pytest.mark.asyncio
async def test_vigilar_command_producto_no_encontrado(monkeypatch):
    monkeypatch.setattr("app.bot.handlers.vigilar.extract_slug_from_url", lambda url: "camiseta-azul-42")
    def raise_value_error(slug):
        raise ValueError
    monkeypatch.setattr("app.bot.handlers.vigilar.get_product_data_from_api", raise_value_error)
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()
    mock_update = MagicMock()
    mock_update.message = mock_message
    mock_update.effective_user.id = 1234
    context = SimpleNamespace(args=["https://fittestfreakest.es/products/camiseta-azul-42"])
    await vigilar_command(mock_update, context)
    mock_message.reply_text.assert_awaited_once_with("❌ No se encontró el producto en la API.")

@pytest.mark.asyncio
async def test_vigilar_command_slug_sin_talla(monkeypatch):
    monkeypatch.setattr("app.bot.handlers.vigilar.extract_slug_from_url", lambda url: "camiseta-azul")
    monkeypatch.setattr("app.bot.handlers.vigilar.get_product_data_from_api", lambda slug: {
        "name": "Camiseta Azul",
        "price": 29.99
    })
    mock_db = MagicMock()
    monkeypatch.setattr("app.bot.handlers.vigilar.SessionLocal", lambda: mock_db)
    fake_user = MagicMock()
    monkeypatch.setattr("app.bot.handlers.vigilar.get_or_create_user", lambda db, tid: fake_user)
    fake_product = MagicMock()
    monkeypatch.setattr("app.bot.handlers.vigilar.add_product_for_user", lambda **kwargs: fake_product)
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()
    mock_update = MagicMock()
    mock_update.message = mock_message
    mock_update.effective_user.id = 1234
    context = SimpleNamespace(args=["https://fittestfreakest.es/products/camiseta-azul"])
    await vigilar_command(mock_update, context)
    mock_message.reply_text.assert_awaited_once()
    text = mock_message.reply_text.call_args[0][0]
    assert "✅ Vigilando producto" in text
    assert "*Camiseta Azul*" in text
    assert "💰 Precio actual: 29.99" in text
    assert "📏 Talla:" not in text