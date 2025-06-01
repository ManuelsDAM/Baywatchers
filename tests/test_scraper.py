from app.scraper import extract_slug_from_url, get_product_data_from_api
import pytest
import requests

def test_extract_slug_from_valid_url():
    url = "https://www.fittestfreakest.es/zapatillas/nike-metcon-9/123456"
    assert extract_slug_from_url(url) == "123456"

def test_extract_slug_from_invalid_url():
    with pytest.raises(ValueError):
        extract_slug_from_url("https://www.fittestfreakest.es/")

class FakeResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json

def test_get_product_data_from_api(monkeypatch):
    def mock_requests_get(url):
        return FakeResponse(
            status_code=200,
            json_data={"name": "Zapatilla de Prueba", "price": 99.99}
        )

    monkeypatch.setattr(requests, "get", mock_requests_get)

    result = get_product_data_from_api("mock-slug")
    assert result["name"] == "Zapatilla de Prueba"
    assert result["price"] == 99.99