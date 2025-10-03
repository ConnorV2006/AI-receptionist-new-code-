"""Seed receptionist user"""

from alembic import op
import sqlalchemy as sa

revision = "0003_seed_receptionist"
down_revision = "0002_seed_roles"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            INSERT INTO "user" (username, email, password, role)
            VALUES ('reception1', 'reception1@example.com', 'pbkdf2:sha256:260000$recept$hashedpass', 'receptionist')
        """)
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role='receptionist'"))
