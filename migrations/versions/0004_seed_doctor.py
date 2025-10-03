"""Seed doctor user"""

from alembic import op
import sqlalchemy as sa

revision = "0004_seed_doctor"
down_revision = "0003_seed_receptionist"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            INSERT INTO "user" (username, email, password, role)
            VALUES ('doctor1', 'doctor1@example.com', 'pbkdf2:sha256:260000$doc$hashedpass', 'doctor')
        """)
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role='doctor'"))
