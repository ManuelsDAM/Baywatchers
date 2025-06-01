import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.api import main as api_module  # Ajusta la importación según tu estructura real

client = TestClient(api_module.app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Baywatchers funcionando"}

def test_get_user_config_found(monkeypatch):
    fake_user = MagicMock(telegram_id=1234, products=[1, 2])
    fake_session = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = fake_user
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)

    response = client.get("/users/1234")
    assert response.status_code == 200
    assert response.json() == {"telegram_id": 1234, "products": 2}

def test_get_user_config_not_found(monkeypatch):
    fake_session = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = None
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)

    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

def test_get_user_products(monkeypatch):
    fake_product = MagicMock(id=1, url="url", last_price=9.99, size="42")
    fake_user = MagicMock(products=[fake_product])
    fake_session = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = fake_user
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)

    response = client.get("/products/1234")
    assert response.status_code == 200
    assert response.json()[0]["url"] == "url"

def test_delete_product(monkeypatch):
    fake_user = MagicMock()
    fake_session = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = fake_user
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)
    monkeypatch.setattr(api_module, "remove_product_for_user", lambda db, user, url: True)

    response = client.request(
        "DELETE",
        "/products/1234",
        json={"url": "https://fake.url"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Producto eliminado"

def test_delete_product_not_found(monkeypatch):
    fake_user = MagicMock()
    fake_session = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = fake_user
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)
    monkeypatch.setattr(api_module, "remove_product_for_user", lambda db, user, url: False)

    response = client.request(
        "DELETE",
        "/products/1234",
        json={"url": "https://fake.url"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"
def test_add_product_success(monkeypatch):
    fake_user = MagicMock()
    fake_product = MagicMock(id=1, url="https://fittestfreakest.es/products/zapatilla-azul-42", last_price=99.99)
    fake_session = MagicMock()
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)
    monkeypatch.setattr(api_module, "get_or_create_user", lambda db, tid: fake_user)
    monkeypatch.setattr(api_module, "extract_slug_from_url", lambda url: "zapatilla-azul-42")
    monkeypatch.setattr(api_module, "get_product_data_from_api", lambda slug: {"price": 99.99})
    monkeypatch.setattr(api_module, "add_product_for_user", lambda **kwargs: fake_product)

    response = client.post(
        "/products/1234",
        json={"url": "https://fittestfreakest.es/products/zapatilla-azul-42"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Producto añadido con éxito"
    assert response.json()["product"]["url"] == "https://fittestfreakest.es/products/zapatilla-azul-42"

def test_add_product_api_error(monkeypatch):
    fake_user = MagicMock()
    fake_session = MagicMock()
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)
    monkeypatch.setattr(api_module, "get_or_create_user", lambda db, tid: fake_user)
    monkeypatch.setattr(api_module, "extract_slug_from_url", lambda url: "zapatilla-azul-42")
    def raise_error(slug):
        raise Exception("API error")
    monkeypatch.setattr(api_module, "get_product_data_from_api", raise_error)

    response = client.post(
        "/products/1234",
        json={"url": "https://fittestfreakest.es/products/zapatilla-azul-42"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No se pudo obtener el producto desde la API"

def test_get_user_products_not_found(monkeypatch):
    fake_session = MagicMock()
    fake_session.query.return_value.filter_by.return_value.first.return_value = None
    monkeypatch.setattr(api_module, "SessionLocal", lambda: fake_session)

    response = client.get("/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"


