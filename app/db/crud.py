from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import User, Product, PriceHistory

def get_or_create_user(db, telegram_id):
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def add_product_for_user(db, user, url, last_price=None, size=None):
    product = Product(url=url, user=user, last_price=last_price, size=size)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def remove_product_for_user(db, user, url):
    product = db.query(Product).filter_by(user=user, url=url).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False

def list_user_products(db, user):
    return db.query(Product).filter_by(user=user).all()

def update_check_interval_for_user(db, user, interval: int) -> int:
    products = db.query(Product).filter(Product.user_id == user.id).all()
    for product in products:
        product.check_interval = interval
    db.commit()
    return len(products)

def get_price_history_for_product(db, product_id: int):
    return db.query(PriceHistory).filter_by(product_id=product_id).order_by(PriceHistory.timestamp.desc()).all()

def get_price_statistics(db, product_id):
    result = db.query(
        func.avg(PriceHistory.price),
        func.max(PriceHistory.price),
        func.min(PriceHistory.price)
    ).filter(PriceHistory.product_id == product_id).first()

    avg, max_, min_ = result
    return round(avg, 2), round(max_, 2), round(min_, 2)

def get_last_10_prices(db, product_id):
    return db.query(PriceHistory)\
        .filter_by(product_id=product_id)\
        .order_by(PriceHistory.timestamp.desc())\
        .limit(10).all()