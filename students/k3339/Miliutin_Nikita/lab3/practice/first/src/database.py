from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
