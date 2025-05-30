from app.bot.telegrambot import main
from app.db import engine
from app.db.models import Base

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()