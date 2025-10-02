"""Add indexes for User table

Revision ID: 0004
Revises: 0003
Create Date: 2025-10-02
"""
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    op.create_index("ix_user_phone", "user", ["phone_number"])


def downgrade():
    op.drop_index("ix_user_phone", table_name="user")
    op.drop_index("ix_user_email", table_name="user")
