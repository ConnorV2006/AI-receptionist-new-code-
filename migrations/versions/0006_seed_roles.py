"""Add roles table and seed default roles

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
    # Create roles table
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), unique=True, nullable=False),
        sa.Column("description", sa.String(length=200)),
    )

    # Add role_id column to user (default staff = 1 later)
    op.add_column("user", sa.Column("role_id", sa.Integer(), sa.ForeignKey("role.id"), nullable=True))

    # Insert default roles
    conn = op.get_bind()
    conn.execute(
        sa.text("INSERT INTO role (name, description) VALUES "
                "('staff', 'Basic staff member with limited access'), "
                "('admin', 'Admin with elevated privileges'), "
                "('superadmin', 'Superadmin with full access')")
    )

    # Set all existing users to staff by default
    conn.execute(sa.text("UPDATE user SET role_id = (SELECT id FROM role WHERE name='staff')"))

    # Make role_id non-nullable after backfilling
    op.alter_column("user", "role_id", nullable=False)


def downgrade():
    # Remove role_id from user
    op.drop_column("user", "role_id")

    # Drop roles table
    op.drop_table("role")
