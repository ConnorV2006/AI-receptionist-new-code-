"""Seed demo doctor

Revision ID: 0005_seed_doctor
Revises: 0004_seed_clinic
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


revision = '0005_seed_doctor'
down_revision = '0004_seed_clinic'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # find doctor role
    role_id = conn.execute(sa.text("SELECT id FROM roles WHERE name='Doctor'")).scalar()
    clinic_id = conn.execute(sa.text("SELECT id FROM clinics WHERE slug='test'")).scalar()

    if role_id and clinic_id:
        conn.execute(sa.text("""
            INSERT INTO users (username, email, password_hash, role_id)
            VALUES (:username, :email, :password_hash, :role_id)
        """), dict(
            username="dr_smith",
            email="drsmith@example.com",
            password_hash=generate_password_hash("DoctorPass123"),
            role_id=role_id
        ))

        user_id = conn.execute(sa.text("SELECT id FROM users WHERE username='dr_smith'")).scalar()
        if user_id:
            conn.execute(sa.text("""
                INSERT INTO doctors (user_id, specialty)
                VALUES (:user_id, :specialty)
            """), dict(user_id=user_id, specialty="General Medicine"))


def downgrade():
    conn = op.get_bind()
    user_id = conn.execute(sa.text("SELECT id FROM users WHERE username='dr_smith'")).scalar()
    if user_id:
        conn.execute(sa.text("DELETE FROM doctors WHERE user_id=:uid"), dict(uid=user_id))
        conn.execute(sa.text("DELETE FROM users WHERE id=:uid"), dict(uid=user_id))
