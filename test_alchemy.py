from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/formulariosenai"

try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("SQLAlchemy conectado!")
    conn.close()
except Exception as e:
    print("Erro SQLAlchemy:", e)
