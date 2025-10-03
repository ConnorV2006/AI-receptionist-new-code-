"""Seed demo clinic, patients, appointments, and doctor notes"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta

revision = "0006_seed_demo_data"
down_revision = "0005_seed_nurse"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Demo patients
    conn.execute(sa.text("""
        INSERT INTO patient (name, email, phone, created_at)
        VALUES 
            ('John Doe', 'john@example.com', '555-1234', :now),
            ('Jane Smith', 'jane@example.com', '555-5678', :now)
    """), {"now": datetime.utcnow()})

    # Demo appointments
    conn.execute(sa.text("""
        INSERT INTO appointment (patient_id, date, notes, created_at)
        VALUES 
            (1, :tomorrow, 'General check-up', :now),
            (2, :nextweek, 'Follow-up visit', :now)
    """), {
        "now": datetime.utcnow(),
        "tomorrow": datetime.utcnow() + timedelta(days=1),
        "nextweek": datetime.utcnow() + timedelta(days=7)
    })


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM appointment"))
    conn.execute(sa.text("DELETE FROM patient"))
