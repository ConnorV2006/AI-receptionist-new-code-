"""Seed default doctor user

Revision ID: 0005_seed_doctor
Revises: 0004_seed_receptionist
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

# revision identifiers
revision = "0005_seed_doctor"
down_revision = "0004_seed_receptionist"
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()
    role_id = connection.execute(sa.text("SELECT id FROM role WHERE name='doctor'")).scalar()
    if role_id:
        connection.execute(
            sa.text(
                "INSERT INTO \"user\" (email, password_hash, role_id) "
                "VALUES (:email, :password_hash, :role_id)"
            ),
            {
                "email": "doctor@example.com",
                "password_hash": generate_password_hash("DoctorPass123!"),
                "role_id": role_id,
            },
        )

def downgrade():
    op.execute("DELETE FROM \"user\" WHERE email='doctor@example.com'")
