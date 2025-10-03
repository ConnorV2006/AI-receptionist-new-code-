"""Seed demo audit logs"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = "0008_seed_audit_logs"
down_revision = "0007_seed_nurse_user"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""
        INSERT INTO audit_log (user, action, details, timestamp)
        VALUES 
            ('admin', 'CREATE_PATIENT', 'Created patient John Doe', :now),
            ('doctor1', 'ADD_NOTE', 'Added follow-up note for Jane Smith', :now),
            ('nurse1', 'CHECK_VITALS', 'Checked vitals for John Doe', :now)
    """), {"now": datetime.utcnow()})


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM audit_log"))
