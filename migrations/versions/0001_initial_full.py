"""Initial full database schema

Revision ID: 0001_initial_full
Revises: 
Create Date: 2025-10-03

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "0001_initial_full"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Roles
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
    )

    # Users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(80), nullable=False, unique=True),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
        sa.Column("password", sa.String(200)),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"), nullable=False),
    )

    # Patients
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(80), nullable=False),
        sa.Column("last_name", sa.String(80), nullable=False),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )

    # Clinics
    op.create_table(
        "clinics",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("twilio_number", sa.String(20)),
        sa.Column("twilio_sid", sa.String(120)),
        sa.Column("twilio_token", sa.String(120)),
    )

    # Appointments
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("scheduled_time", sa.DateTime, nullable=False),
    )

    # Doctor Notes
    op.create_table(
        "doctor_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
    )

    # Nurse Profiles
    op.create_table(
        "nurse_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("nurse_id", sa.String(50), unique=True, nullable=False),
    )

    # Receptionist Profiles
    op.create_table(
        "receptionist_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("receptionist_id", sa.String(50), unique=True, nullable=False),
    )

    # Audit Logs
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("action", sa.String(120), nullable=False),
        sa.Column("details", sa.Text),
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow),
    )

    # Fax Logs
    op.create_table(
        "fax_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sender", sa.String(120), nullable=False),
        sa.Column("recipient", sa.String(120), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),  # sent, received, failed, scheduled
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow, nullable=False),
    )


def downgrade():
    op.drop_table("fax_logs")
    op.drop_table("audit_logs")
    op.drop_table("receptionist_profiles")
    op.drop_table("nurse_profiles")
    op.drop_table("doctor_notes")
    op.drop_table("appointments")
    op.drop_table("clinics")
    op.drop_table("patients")
    op.drop_table("users")
    op.drop_table("roles")
