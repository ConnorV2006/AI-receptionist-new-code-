"""Seed demo patients & appointments"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

revision = "0006_seed_demo_data"
down_revision = "0005_seed_nurse"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute(sa.text("""
        INSERT INTO patient (name, email, phone, created_at)
        VALUES ('John Doe', 'john@example.com', '555-1234', :now)
    """), {"now": datetime.utcnow()})

    conn.execute(sa.text("""
        INSERT INTO appointment (patient_id, date, notes, created_at)
        VALUES (1, :appt_time, 'Initial Consultation', :now)
    """), {
        "appt_time": datetime.utcnow() + timedelta(days=1),
        "now": datetime.utcnow()
    })


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM appointment"))
    conn.execute(sa.text("DELETE FROM patient"))
