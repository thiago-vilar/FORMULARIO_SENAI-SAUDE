# backend/migrations/env.py

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os
# Adiciona o caminho da pasta backend ao sys.path para encontrar os models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa os modelos do projeto
from app.models.base import Base
from app.models.formulario import Formulario
from app.models.campo import Campo
from app.models.resposta import Resposta

# Este é o objeto de configuração do Alembic
config = context.config

# Interpreta o arquivo de configuração para logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o target_metadata para autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa as migrations no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa as migrations no modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
