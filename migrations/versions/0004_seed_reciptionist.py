"""Seed default receptionist user

Revision ID: 0004_seed_receptionist
Revises: 0003_seed_superadmin
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

# revision identifiers
revision = "0004_seed_receptionist"
down_revision = "0003_seed_superadmin"
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()
    role_id = connection.execute(sa.text("SELECT id FROM role WHERE name='receptionist'")).scalar()
    if role_id:
        connection.execute(
            sa.text(
                "INSERT INTO \"user\" (email, password_hash, role_id) "
                "VALUES (:email, :password_hash, :role_id)"
            ),
            {
                "email": "receptionist@example.com",
                "password_hash": generate_password_hash("Reception123!"),
                "role_id": role_id,
            },
        )

def downgrade():
    op.execute("DELETE FROM \"user\" WHERE email='receptionist@example.com'")
