"""Seed default clinic

Revision ID: 0004_seed_clinic
Revises: 0003_seed_admin
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa


revision = '0004_seed_clinic'
down_revision = '0003_seed_admin'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO clinics (name, slug)
        VALUES (:name, :slug)
    """), dict(name="Test Clinic", slug="test"))


def downgrade():
    op.execute("DELETE FROM clinics WHERE slug='test'")
