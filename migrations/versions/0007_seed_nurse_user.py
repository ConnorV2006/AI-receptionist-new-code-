"""Seed nurse role user"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0007_seed_nurse_user"
down_revision = "0006_seed_doctor"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Insert a sample nurse user
    conn.execute(
        sa.text("""
            INSERT INTO "user" (username, email, password, role)
            VALUES (
                'nurse1',
                'nurse1@example.com',
                -- Replace with a real hashed password later!
                'pbkdf2:sha256:260000$example$hashedpasswordhere',
                'nurse'
            )
        """)
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM \"user\" WHERE email='nurse1@example.com'"))
