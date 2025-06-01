import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from app.bot.handlers.checkinterval import checkinterval_command
from app.db.models import Base, User as DBUser, Product
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
async def test_checkinterval_valido(monkeypatch, db):
    # Crear usuario y producto
    user = DBUser(telegram_id=1234)
    db.add(user)
    db.commit()

    product = Product(url="https://producto.com", user_id=user.id, check_interval=60)
    db.add(product)
    db.commit()

    # Crear mocks de update y message
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_message
    mock_update.effective_user.id = 1234

    # Crear contexto simulado
    context = SimpleNamespace()
    context.args = ["30"]

    # Usar la base de datos de prueba
    monkeypatch.setattr("app.bot.handlers.checkinterval.SessionLocal", lambda: db)

    # Ejecutar el handler
    await checkinterval_command(mock_update, context)

    # Verificar el mensaje de respuesta
    mock_message.reply_text.assert_called_once()
    assert "actualizado a 30 minutos" in mock_message.reply_text.call_args[0][0]
