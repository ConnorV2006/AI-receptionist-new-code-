"""Add phone_number to User

Revision ID: 0002
Revises: 0001
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user", sa.Column("phone_number", sa.String(length=20)))


def downgrade():
    op.drop_column("user", "phone_number")
