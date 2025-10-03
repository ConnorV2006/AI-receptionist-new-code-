"""Seed nurse user"""

from alembic import op
import sqlalchemy as sa

revision = "0005_seed_nurse"
down_revision = "0004_seed_doctor"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            INSERT INTO "user" (username, email, password, role)
            VALUES ('nurse1', 'nurse1@example.com', 'pbkdf2:sha256:260000$nurse$hashedpass', 'nurse')
        """)
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE role='nurse'"))
