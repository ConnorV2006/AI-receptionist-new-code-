from __future__ import with_statement
import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import db  # <-- Import your SQLAlchemy instance

# Alembic Config object, provides access to the .ini file
config = context.config

# Interpret logging configuration from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your models here so Alembic knows about them
target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    Uses the DATABASE_URL env var directly.
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is not set!")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with a live connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=os.getenv("DATABASE_URL"),
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
