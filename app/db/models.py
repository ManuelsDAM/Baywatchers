from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    products = relationship("Product", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    size = Column(String, nullable=True)
    last_price = Column(Float, nullable=True)
    check_interval = Column(Integer, default=60)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="products")
