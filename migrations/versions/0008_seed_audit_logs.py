"""Seed audit logs"""

from alembic import op
import sqlalchemy as sa
import datetime

# Revision identifiers
revision = '0008_seed_audit_logs'
down_revision = '0007_add_nurse_table'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    now = datetime.datetime.utcnow()

    conn.execute(sa.text("""
        INSERT INTO audit_log (user, action, timestamp, details)
        VALUES
          ('superadmin', 'CREATE_PATIENT', :t1, 'Created patient Alice Johnson'),
          ('receptionist', 'SCHEDULE_APPOINTMENT', :t2, 'Scheduled appointment for Bob Smith'),
          ('doctor', 'ADD_NOTE', :t3, 'Added note for Carol Davis appointment'),
          ('nurse', 'CHECK_VITALS', :t4, 'Recorded vitals for Alice Johnson')
    """), {
        "t1": now - datetime.timedelta(days=2),
        "t2": now - datetime.timedelta(days=1),
        "t3": now - datetime.timedelta(hours=6),
        "t4": now - datetime.timedelta(minutes=30),
    })

def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM audit_log"))
