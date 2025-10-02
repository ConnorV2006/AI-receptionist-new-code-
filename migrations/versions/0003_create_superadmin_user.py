"""Create default superadmin user

Revision ID: 0003_create_superadmin_user
Revises: 0002_seed_roles
Create Date: 2025-10-02

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


# Revision identifiers
revision = "0003_create_superadmin_user"
down_revision = "0002_seed_roles"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # Get the superadmin role ID
    role_id = connection.execute(
        sa.text("SELECT id FROM role WHERE name='superadmin'")
    ).scalar()

    if role_id:
        password_hash = generate_password_hash("ChangeMe123!")  # default password
        connection.execute(
            sa.text(
                "INSERT INTO \"user\" (email, password_hash, role_id) "
                "VALUES (:email, :password_hash, :role_id)"
            ),
            {"email": "superadmin@example.com", "password_hash": password_hash, "role_id": role_id},
        )


def downgrade():
    op.execute("DELETE FROM \"user\" WHERE email='superadmin@example.com'")
