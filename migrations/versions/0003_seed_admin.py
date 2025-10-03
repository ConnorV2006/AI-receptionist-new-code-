"""Seed initial admin user

Revision ID: 0003_seed_admin
Revises: 0002_seed_roles
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


revision = '0003_seed_admin'
down_revision = '0002_seed_roles'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    role_id = conn.execute(sa.text("SELECT id FROM roles WHERE name='Admin'")).scalar()
    if role_id:
        conn.execute(sa.text("""
            INSERT INTO users (username, email, password_hash, role_id)
            VALUES (:username, :email, :password_hash, :role_id)
        """), dict(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("StrongP@ssw0rd!"),
            role_id=role_id
        ))


def downgrade():
    op.execute("DELETE FROM users WHERE username='admin'")
