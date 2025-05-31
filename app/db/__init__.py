from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./baywatchers.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Requerido por SQLite para usar sesiones en hilos
    echo=False  # Opcional: True si quieres ver las consultas SQL por consola
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
