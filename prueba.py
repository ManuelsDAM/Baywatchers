from app.db import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)
print("Tablas creadas con éxito.")
