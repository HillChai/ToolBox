# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings
from sqlalchemy.engine import make_url

DATABASE_URL = str(settings.DATABASE_URL)
url = make_url(DATABASE_URL)

engine = create_engine(
    url,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
