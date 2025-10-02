"""Add clinic_id foreign key to User

Revision ID: 0003
Revises: 0002
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user", sa.Column("clinic_id", sa.Integer(), sa.ForeignKey("clinic.id")))


def downgrade():
    op.drop_column("user", "clinic_id")
