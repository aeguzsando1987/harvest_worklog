# temp_check.py
from app.database.database import Base
print("Registered tables:", list(Base.metadata.tables.keys()))