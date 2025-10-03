"""Add partial index for future appointments on (doctor_id, scheduled_time)

Revision ID: 0012_add_partial_future_index
Revises: 0011_add_doctor_time_composite
Create Date: 2025-10-03
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0012_add_partial_future_index"
down_revision = "0011_add_doctor_time_composite"
branch_labels = None
depends_on = None


def upgrade():
    # Partial index: only future appointments
    op.execute(
        """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_appointments_doctor_scheduled_future
        ON appointments (doctor_id, scheduled_time)
        WHERE scheduled_time >= NOW();
        """
    )


def downgrade():
    op.execute(
        "DROP INDEX CONCURRENTLY IF EXISTS ix_appointments_doctor_scheduled_future;"
    )
