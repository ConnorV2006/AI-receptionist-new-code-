"""Seed demo nurse

Revision ID: 0006_seed_nurse
Revises: 0005_seed_doctor
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


revision = '0006_seed_nurse'
down_revision = '0005_seed_doctor'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    role_id = conn.execute(sa.text("SELECT id FROM roles WHERE name='Nurse'")).scalar()
    if role_id:
        conn.execute(sa.text("""
            INSERT INTO users (username, email, password_hash, role_id)
            VALUES (:username, :email, :password_hash, :role_id)
        """), dict(
            username="nurse_anna",
            email="nurseanna@example.com",
            password_hash=generate_password_hash("NursePass123"),
            role_id=role_id
        ))

        user_id = conn.execute(sa.text("SELECT id FROM users WHERE username='nurse_anna'")).scalar()
        if user_id:
            conn.execute(sa.text("""
                INSERT INTO nurses (user_id)
                VALUES (:user_id)
            """), dict(user_id=user_id))


def downgrade():
    conn = op.get_bind()
    user_id = conn.execute(sa.text("SELECT id FROM users WHERE username='nurse_anna'")).scalar()
    if user_id:
        conn.execute(sa.text("DELETE FROM nurses WHERE user_id=:uid"), dict(uid=user_id))
        conn.execute(sa.text("DELETE FROM users WHERE id=:uid"), dict(uid=user_id))
