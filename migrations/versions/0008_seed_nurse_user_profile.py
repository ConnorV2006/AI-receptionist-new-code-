"""Seed nurse user and profile"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0008_seed_nurse_user_profile"
down_revision = "0007_add_nurse_profile"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Insert nurse user
    conn.execute(sa.text("""
        INSERT INTO "user" (id, username, email, password, role)
        VALUES (
            1001,
            'nurse1',
            'nurse1@example.com',
            'pbkdf2:sha256:260000$demo$hashedpass',
            'nurse'
        )
    """))

    # Insert nurse profile linked to user_id=1001
    conn.execute(sa.text("""
        INSERT INTO nurse (user_id, specialty, shift, license_number)
        VALUES (1001, 'General', 'Day', 'RN-12345')
    """))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM nurse WHERE user_id=1001"))
    conn.execute(sa.text("DELETE FROM \"user\" WHERE id=1001"))
