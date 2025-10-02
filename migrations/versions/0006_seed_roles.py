"""Seed default user roles

Revision ID: 0006
Revises: 0005
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    # Insert default roles by convention (not enforced by schema)
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO user (email, password_hash, role) "
            "VALUES (:email, :password_hash, :role)"
        ),
        [
            {"email": "staff@example.com", "password_hash": "changeme", "role": "staff"},
            {"email": "admin@example.com", "password_hash": "changeme", "role": "admin"},
            {"email": "superadmin@example.com", "password_hash": "changeme", "role": "superadmin"},
        ],
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM user WHERE email IN "
                "('staff@example.com','admin@example.com','superadmin@example.com')")
    )
