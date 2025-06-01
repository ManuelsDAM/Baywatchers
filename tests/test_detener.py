import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from app.bot.handlers.detener import detener_command  # Ajusta el import si está en otro archivo
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
async def test_detener_command_producto_eliminado(monkeypatch, db):
    # Crear usuario y producto en la base de datos
    user = DBUser(telegram_id=1234)
    db.add(user)
    db.commit()

    product = Product(url="https://producto.com", user_id=user.id, check_interval=60)
    db.add(product)
    db.commit()

    # Mock de update y message
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_message
    mock_update.effective_user.id = 1234

    # Context simulado con la URL a detener
    context = SimpleNamespace()
    context.args = ["https://producto.com"]

    # Parchear SessionLocal para que devuelva nuestra sesión de prueba
    monkeypatch.setattr("app.bot.handlers.detener.SessionLocal", lambda: db)

    # Ejecutar el comando
    await detener_command(mock_update, context)

    # Verificar que el mensaje fue el correcto
    mock_message.reply_text.assert_called_once()
    respuesta = mock_message.reply_text.call_args[0][0]
    assert "Dejaste de vigilar el producto" in respuesta

    # Verificar que el producto fue eliminado de la base de datos
    assert db.query(Product).filter_by(url="https://producto.com").first() is None
