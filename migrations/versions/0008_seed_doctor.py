"""Seed a default doctor account

Revision ID: 0008_seed_doctor
Revises: 0007_add_doctor_notes
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

# Revision identifiers
revision = "0008_seed_doctor"
down_revision = "0007_add_doctor_notes"
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()

    # ensure doctor role exists
    role_id = connection.execute(
        sa.text("SELECT id FROM role WHERE name='doctor'")
    ).scalar()
    if not role_id:
        connection.execute(
            sa.text("INSERT INTO role (name) VALUES ('doctor')")
        )
        role_id = connection.execute(
            sa.text("SELECT id FROM role WHERE name='doctor'")
        ).scalar()

    password_hash = generate_password_hash("DoctorPass123!")
    connection.execute(
        sa.text(
            "INSERT INTO \"user\" (email, password_hash, role_id) "
            "VALUES (:email, :password_hash, :role_id)"
        ),
        {"email": "doctor@example.com", "password_hash": password_hash, "role_id": role_id},
    )

def downgrade():
    op.execute("DELETE FROM \"user\" WHERE email='doctor@example.com'")
