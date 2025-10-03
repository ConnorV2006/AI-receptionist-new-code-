"""Seed initial audit log entries

Revision ID: 0007_seed_audit_logs
Revises: 0006_seed_nurse
Create Date: 2025-10-02
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


revision = '0007_seed_audit_logs'
down_revision = '0006_seed_nurse'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    admin_id = conn.execute(sa.text("SELECT id FROM users WHERE username='admin'")).scalar()
    if admin_id:
        conn.execute(sa.text("""
            INSERT INTO audit_logs (user_id, action, timestamp, details)
            VALUES (:uid, :action, :ts, :details)
        """), dict(
            uid=admin_id,
            action="System Initialized",
            ts=datetime.utcnow(),
            details="Initial migration and seeding complete"
        ))


def downgrade():
    op.execute("DELETE FROM audit_logs WHERE action='System Initialized'")
