# tests/conftest.py

import os
import types
import importlib
import contextlib
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from starlette.testclient import TestClient

# 1) Força o ambiente de teste
os.environ.setdefault("ENV", "test")

# 2) Importa app e Base usando caminho total do projeto
#    (isso garante compatibilidade com a sua estrutura atual)
from backend.app.main import app  # type: ignore
from backend.app.models.base import Base  # type: ignore

# 3) Vamos substituir o SessionLocal do projeto por um SessionLocal de teste (SQLite em memória)
#    - Mantém o padrão de uso do app, sem tocar no Postgres real
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:?cache=shared"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    future=True,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


# 4) Utilitário para fazer override do SessionLocal EXPÕE a mesma assinatura do projeto
def _override_session_local():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 5) Alguns projetos expõem o SessionLocal em backend.app.db.session.SessionLocal,
#    outros via um get_db dependency. Cobrimos os dois casos:
@pytest.fixture(scope="session", autouse=True)
def override_sessionlocal_module() -> Generator[None, None, None]:
    """
    Substitui backend.app.db.session.SessionLocal por nossa TestingSessionLocal.
    Isso cobre casos onde os controllers importam diretamente SessionLocal do módulo.
    """
    session_mod = importlib.import_module("backend.app.db.session")
    # backup
    original = getattr(session_mod, "SessionLocal", None)
    setattr(session_mod, "SessionLocal", TestingSessionLocal)
    try:
        yield
    finally:
        if original is not None:
            setattr(session_mod, "SessionLocal", original)


@pytest.fixture(scope="session", autouse=True)
def create_all_tables() -> Generator[None, None, None]:
    """
    Cria todas as tabelas uma vez por sessão de testes.
    """
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def db_clean() -> Generator[None, None, None]:
    """
    Limpa o estado entre testes recriando as tabelas.
    Simples e robusto para projeto em evolução.
    """
    # Drop + create por teste evita “vazameno” entre cenários
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Cliente HTTP para testes de integração.
    Se seu app usa Depends(get_db), mantenha assim;
    se usa SessionLocal direto (módulo), já cobrimos acima.
    """
    # App tem uma dependência get_db, fazer override aqui:
    # Exemplo:
    #
    # from fastapi import Depends
    # def get_db():
    #     yield from _override_session_local()
    # app.dependency_overrides[get_db] = lambda: _override_session_local()

    with TestClient(app) as c:
        yield c
