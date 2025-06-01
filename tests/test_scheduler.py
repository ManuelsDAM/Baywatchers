# test_scheduler.py

import pytest
from unittest.mock import patch, MagicMock
from app.scheduler import track_product, reprogram_all_jobs

@patch("app.scheduler.SessionLocal")
@patch("app.scheduler.extract_slug_from_url")
@patch("app.scheduler.get_product_data_from_api")
@patch("app.scheduler.send_message")
def test_track_product_price_change(mock_send_message, mock_get_data, mock_extract_slug, mock_session):
    # Setup mocks
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    # Fake product in DB
    product = MagicMock()
    product.id = 1
    product.url = "https://fittestfreakest.com/product/example"
    product.user_id = 10
    product.last_price = 100
    mock_db.query().filter_by().first.return_value = product

    # Fake user
    user = MagicMock()
    user.telegram_id = 12345
    mock_db.query().filter_by().first.side_effect = [product, user]

    # Fake API data
    mock_extract_slug.return_value = "example"
    mock_get_data.return_value = {"price": 90, "name": "Zapatilla Pro"}

    # Ejecutar
    track_product(1)

    # Verificaciones
    mock_send_message.assert_called_once()
    assert product.last_price == 90
    mock_db.commit.assert_called_once()

@patch("app.scheduler.SessionLocal")
@patch("app.scheduler.scheduler")
def test_reprogram_all_jobs(mock_scheduler, mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    # Fake products
    p1 = MagicMock(id=1, url="url1", check_interval=5)
    p2 = MagicMock(id=2, url="url2", check_interval=10)
    mock_db.query().all.return_value = [p1, p2]

    # Ejecutar
    reprogram_all_jobs()

    # Verificaciones
    mock_scheduler.remove_all_jobs.assert_called_once()
    assert mock_scheduler.add_job.call_count == 2
