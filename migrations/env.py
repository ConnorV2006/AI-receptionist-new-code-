from __future__ import with_statement
import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from flask import current_app

# Interpret config file for Python logging.
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

logger = logging.getLogger('alembic.env')

# Get the SQLAlchemy connection from Flask app
config = context.config
target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = current_app.extensions['migrate'].db.engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
