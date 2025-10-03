"""Add doctor_notes and nurse_profiles tables

Revision ID: 0008_add_notes_profiles
Revises: 0007_seed_audit_logs
Create Date: 2025-10-03
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0008_add_notes_profiles"
down_revision = "0007_seed_audit_logs"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "doctor_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("doctors.id"), nullable=False),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("appointment_id", sa.Integer, sa.ForeignKey("appointments.id"), nullable=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "nurse_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nurse_id", sa.Integer, sa.ForeignKey("nurses.id"), nullable=False),
        sa.Column("bio", sa.Text),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("nurse_profiles")
    op.drop_table("doctor_notes")
