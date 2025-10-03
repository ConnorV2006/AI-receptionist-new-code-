"""Seed sample audit logs"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# Revision identifiers
revision = "0009_seed_audit_logs"
down_revision = "0008_seed_nurse_user_profile"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    now = datetime.utcnow()

    sample_logs = [
        ("admin", "CREATE_PATIENT", "Created patient John Doe", now),
        ("doctor1", "ADD_NOTE", "Added consultation note for John Doe", now),
        ("reception1", "SCHEDULE_APPOINTMENT", "Scheduled John Doe for tomorrow", now),
        ("nurse1", "CHECK_VITALS", "Recorded vitals for John Doe", now),
        ("superadmin", "MANAGE_USERS", "Granted access to new doctor account", now),
    ]

    for user, action, details, ts in sample_logs:
        conn.execute(
            sa.text("""
                INSERT INTO audit_log (user, action, details, timestamp)
                VALUES (:user, :action, :details, :ts)
            """),
            {"user": user, "action": action, "details": details, "ts": ts}
        )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM audit_log WHERE user IN ('admin','doctor1','reception1','nurse1','superadmin')"))
