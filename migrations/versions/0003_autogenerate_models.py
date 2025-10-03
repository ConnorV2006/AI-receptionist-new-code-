"""Sync schema with updated models.py (add receptionist, twilio logs, indexes)

Revision ID: 0003_autogenerate_models
Revises: 0002_seed_demo_data
Create Date: 2025-10-03
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0003_autogenerate_models"
down_revision = "0002_seed_demo_data"
branch_labels = None
depends_on = None


def upgrade():
    # --- Receptionist Profiles ---
    op.create_table(
        "receptionist_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), unique=True),
        sa.Column("receptionist_id", sa.String(length=50), unique=True, nullable=False),
    )

    # --- Twilio Logs ---
    op.create_table(
        "twilio_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("direction", sa.String(length=20), nullable=False),
        sa.Column("from_number", sa.String(length=20), nullable=False),
        sa.Column("to_number", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("status", sa.String(length=50)),
        sa.Column("timestamp", sa.DateTime, server_default=sa.func.now(), index=True),
    )

    # --- Indexes (appointments composite already in 0011/0012, keep consistent) ---
    op.create_index(
        "ix_appointments_doctor_time",
        "appointments",
        ["doctor_id", "scheduled_time"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_appointments_doctor_time", table_name="appointments")
    op.drop_table("twilio_logs")
    op.drop_table("receptionist_profiles")
