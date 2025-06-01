import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, Product, PriceHistory
from app.db.crud import get_price_statistics, get_last_10_prices

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    yield db
    db.close()

def test_price_statistics_and_history(db):
    user = User(telegram_id=1111)
    product = Product(url="https://test.com", user=user)
    db.add(user)
    db.add(product)
    db.commit()

    precios = [10, 12, 15, 13, 11, 14, 18, 16, 19, 20]
    for p in precios:
        db.add(PriceHistory(product_id=product.id, price=p))
    db.commit()

    avg, max_, min_ = get_price_statistics(db, product.id)
    assert round(avg, 2) == 14.8
    assert max_ == 20
    assert min_ == 10

    last_prices = get_last_10_prices(db, product.id)
    assert len(last_prices) == 10
