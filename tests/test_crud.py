import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.db.crud import get_or_create_user, add_product_for_user, list_user_products

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    yield db
    db.close()

def test_get_or_create_user(db):
    user = get_or_create_user(db, telegram_id=123456)
    assert user.telegram_id == 123456

def test_add_product_for_user(db):
    user = get_or_create_user(db, telegram_id=789)
    product = add_product_for_user(db, user, url="https://example.com")
    assert product.url == "https://example.com"

def test_list_user_products(db):
    user = get_or_create_user(db, telegram_id=456)
    add_product_for_user(db, user, url="https://1.com")
    add_product_for_user(db, user, url="https://2.com")
    products = list_user_products(db, user)
    assert len(products) == 2
