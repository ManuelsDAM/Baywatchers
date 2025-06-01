import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from app.bot.handlers.misproductos import misproductos_command
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
async def test_misproductos_command_con_productos(monkeypatch, db):
    # Crear usuario y productos
    user = DBUser(telegram_id=1234)
    db.add(user)
    db.commit()

    urls = ["https://a.com", "https://b.com"]
    for url in urls:
        p = Product(url=url, user_id=user.id)
        db.add(p)
    db.commit()

    # Mocks
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_message
    mock_update.effective_user.id = 1234

    context = SimpleNamespace()

    # Parchar SessionLocal
    monkeypatch.setattr("app.bot.handlers.misproductos.SessionLocal", lambda: db)

    await misproductos_command(mock_update, context)

    mock_message.reply_text.assert_called_once()
    respuesta = mock_message.reply_text.call_args[0][0]
    assert "🛒 Productos que vigilas" in respuesta
    assert "- https://a.com" in respuesta
    assert "- https://b.com" in respuesta
