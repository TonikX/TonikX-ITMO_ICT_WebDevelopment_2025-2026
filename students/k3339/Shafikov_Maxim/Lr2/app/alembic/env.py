import os
from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from app.db.base import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

target_metadata = Base.metadata

# Синхронный движок
engine = create_engine(DATABASE_URL, future=True)


def run_migrations_online():
    with engine.connect() as connection:
        do_run_migrations(connection)


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()
