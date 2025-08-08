# backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class DatabaseSessionFactory:
    _engine = None
    _sessionmaker = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            user = os.getenv("POSTGRES_USER", "postgres")
            password = os.getenv("POSTGRES_PASSWORD", "postgres")
            host = os.getenv("POSTGRES_HOST", "localhost")
            db = os.getenv("POSTGRES_DB", "formulariosenai")
            url = f"postgresql+psycopg2://{user}:{password}@{host}/{db}"
            cls._engine = create_engine(url, future=True)
        return cls._engine

    @classmethod
    def get_sessionmaker(cls):
        if cls._sessionmaker is None:
            engine = cls.get_engine()
            cls._sessionmaker = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        return cls._sessionmaker

    def __call__(self):
        sessionmaker_ = self.get_sessionmaker()
        return sessionmaker_()
