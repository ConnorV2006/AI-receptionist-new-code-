"""Seed nurse profile"""

from alembic import op
import sqlalchemy as sa

revision = "0008_seed_nurse_user_profile"
down_revision = "0007_add_nurse_profile"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # attach profile to nurse1
    nurse_id = conn.execute(sa.text("SELECT id FROM \"user\" WHERE email='nurse1@example.com'")).scalar()

    if nurse_id:
        conn.execute(sa.text("""
            INSERT INTO nurse (user_id, specialty, shift, license_number)
            VALUES (:uid, 'General', 'Day', 'RN-12345')
        """), {"uid": nurse_id})


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM nurse WHERE license_number='RN-12345'"))
