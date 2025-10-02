"""Add audit_log table for superadmin visibility

Revision ID: 0005
Revises: 0004
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id")),
        sa.Column("action", sa.String(length=200), nullable=False),
        sa.Column("details", sa.Text()),
        sa.Column("timestamp", sa.DateTime(), default=datetime.utcnow, nullable=False),
    )
    op.create_index("ix_audit_user", "audit_log", ["user_id"])
    op.create_index("ix_audit_timestamp", "audit_log", ["timestamp"])


def downgrade():
    op.drop_index("ix_audit_timestamp", table_name="audit_log")
    op.drop_index("ix_audit_user", table_name="audit_log")
    op.drop_table("audit_log")
