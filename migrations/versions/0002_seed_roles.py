"""Seed default roles"""

from alembic import op
import sqlalchemy as sa

revision = "0002_seed_roles"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Insert roles as example users (roles are tracked in user table)
    conn.execute(
        sa.text("""
            INSERT INTO "user" (username, email, password, role)
            VALUES 
                ('admin', 'admin@example.com', 'pbkdf2:sha256:260000$admin$hashedpass', 'admin'),
                ('superadmin', 'superadmin@example.com', 'pbkdf2:sha256:260000$super$hashedpass', 'superadmin')
        """)
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role IN ('admin','superadmin')"))
