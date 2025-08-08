# backend/app/db/init_db.py

from backend.app.models.base import Base
from backend.app.db.session import DatabaseSessionFactory

def init_db():
    """Cria todas as tabelas declaradas no Base."""
    engine = DatabaseSessionFactory.get_engine()
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()
