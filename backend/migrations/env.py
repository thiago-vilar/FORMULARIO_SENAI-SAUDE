import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use DATABASE_URL se existir
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

from app.models.base import Base  # mantenha seus imports
target_metadata = Base.metadata
...
