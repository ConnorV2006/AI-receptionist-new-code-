"""Seed default roles

Revision ID: 0002_seed_roles
Revises: 0001_initial_schema
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "0002_seed_roles"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()
    roles = ["superadmin", "receptionist", "doctor"]
    for role in roles:
        connection.execute(
            sa.text("INSERT INTO role (name) VALUES (:name) ON CONFLICT DO NOTHING"),
            {"name": role},
        )

def downgrade():
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM role WHERE name IN ('superadmin','receptionist','doctor')"))
