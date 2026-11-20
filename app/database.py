from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from configs.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo = True)
SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

def get_session():
    with SessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass
