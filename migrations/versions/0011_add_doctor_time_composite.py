"""Add composite index (doctor_id, scheduled_time) for appointments (concurrent)

Revision ID: 0011_add_doctor_time_composite
Revises: 0010_add_indexes
Create Date: 2025-10-03
"""
from alembic import op

# Revision identifiers, used by Alembic.
revision = "0011_add_doctor_time_composite"
down_revision = "0010_add_indexes"
branch_labels = None
depends_on = None


def upgrade():
    # Create composite index concurrently with AUTOCOMMIT
    op.execute(
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_appointments_doctor_time
        ON appointments (doctor_id, scheduled_time);
        """,
        execution_options={"isolation_level": "AUTOCOMMIT"}
    )


def downgrade():
    # Drop index concurrently with AUTOCOMMIT
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_appointments_doctor_time;",
        execution_options={"isolation_level": "AUTOCOMMIT"}
    )
