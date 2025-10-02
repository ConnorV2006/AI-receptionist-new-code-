"""Seed default roles

Revision ID: 0002_seed_roles
Revises: 0001_initial
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = "0002_seed_roles"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    # Insert default roles
    op.execute("INSERT INTO role (name) VALUES ('superadmin')")
    op.execute("INSERT INTO role (name) VALUES ('admin')")
    op.execute("INSERT INTO role (name) VALUES ('staff')")


def downgrade():
    # Remove seeded roles
    op.execute("DELETE FROM role WHERE name IN ('superadmin', 'admin', 'staff')")
