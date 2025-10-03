"""Add composite index (doctor_id, scheduled_time) for appointments (concurrent)

Revision ID: 0011_add_doctor_time_composite
Revises: 0010_add_indexes
Create Date: 2025-10-03
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0011_add_doctor_time_composite"
down_revision = "0010_add_indexes"
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.create_index(
            "ix_appointments_doctor_time",
            "appointments",
            ["doctor_id", "scheduled_time"],
            postgresql_concurrently=True,
        )


def downgrade():
    op.drop_index("ix_appointments_doctor_time", table_name="appointments")
