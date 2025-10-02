from __future__ import with_statement
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your app + models
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # add project root to path
from app import app, db  # <-- make sure app and db are imported
import models  # <-- imports all models so Alembic can autogenerate migrations

# Alembic Config object
config = context.config

# ✅ Try to load alembic.ini if it exists
if config.config_file_name and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = db.metadata


def get_url():
    """Get database URL from environment (DATABASE_URL)."""
    return os.getenv("DATABASE_URL", "sqlite:///app.db")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),  # override with env var
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Choose offline vs online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
