from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the project root to PYTHONPATH so imports work
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import db  # import your SQLAlchemy db instance

# Alembic Config object
config = context.config

# Point Alembic to the root-level alembic.ini
ini_path = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
if os.path.exists(ini_path):
    fileConfig(ini_path)

# Set target metadata for autogenerate
target_metadata = db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url") or os.getenv("DATABASE_URL")
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
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=os.getenv("DATABASE_URL"),  # Use your env var for DB URL
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
