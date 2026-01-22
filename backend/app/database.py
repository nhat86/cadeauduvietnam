import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

POSTGRES_USER = os.getenv("POSTGRES_USER", "nhat")
POSTGRES_PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", "Nhat1986"))  # đổi password mới
POSTGRES_DB = os.getenv("POSTGRES_DB", "cadeauduvietnam")

# Kết nối tới container 'db' trong Docker Compose
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
