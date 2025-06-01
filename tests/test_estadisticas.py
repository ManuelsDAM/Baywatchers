import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from app.bot.handlers.estadisticas import estadisticas_command  # Ajusta según tu estructura
from app.db.models import Base, User as DBUser, Product, PriceHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)
    db = TestingSession()
    yield db
    db.close()

@pytest.mark.asyncio
async def test_estadisticas_command_producto_vigilado(monkeypatch, db):
    # Crear usuario y producto
    user = DBUser(telegram_id=1234)
    db.add(user)
    db.commit()

    product = Product(url="https://producto.com", user_id=user.id)
    db.add(product)
    db.commit()

    # Añadir historial de precios
    now = datetime.now()
    for i in range(5):
        price = PriceHistory(product_id=product.id, price=100 + i * 5, timestamp=now)
        db.add(price)
    db.commit()

    # Mock de update y message
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_message
    mock_update.effective_user.id = 1234

    # Context simulado
    context = SimpleNamespace()
    context.args = ["https://producto.com"]

    # Parchear SessionLocal
    monkeypatch.setattr("app.bot.handlers.estadisticas.SessionLocal", lambda: db)

    # Ejecutar el comando
    await estadisticas_command(mock_update, context)

    # Verificar que se llamó reply_text con datos esperados
    mock_message.reply_text.assert_called_once()
    response = mock_message.reply_text.call_args[0][0]
    assert "📊 Estadísticas para" in response
    assert "Precio medio" in response
    assert "Últimos 10 precios" in response
