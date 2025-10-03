"""Initial full schema with all tables

Revision ID: 0001_initial_full
Revises: 
Create Date: 2025-10-03
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial_full"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # --- Roles ---
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
    )

    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(80), unique=True, nullable=False),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(128), nullable=False),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_created_at", "users", ["created_at"])

    # --- Patients ---
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(120), unique=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("date_of_birth", sa.Date),
    )
    op.create_index("ix_patients_email", "patients", ["email"])
    op.create_index("ix_patients_last_name", "patients", ["last_name"])

    # --- Appointments ---
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("doctor_id", sa.Integer, nullable=False),
        sa.Column("scheduled_time", sa.DateTime, nullable=False),
        sa.Column("reason", sa.String(255)),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_scheduled_time", "appointments", ["scheduled_time"])

    # --- Doctor Notes ---
    op.create_table(
        "doctor_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("doctor_id", sa.Integer, nullable=False),
        sa.Column("note", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_doctor_notes_patient_id", "doctor_notes", ["patient_id"])
    op.create_index("ix_doctor_notes_doctor_id", "doctor_notes", ["doctor_id"])
    op.create_index("ix_doctor_notes_created_at", "doctor_notes", ["created_at"])

    # --- Nurse Profiles ---
    op.create_table(
        "nurse_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("nurse_id", sa.String(50), unique=True),
    )
    op.create_index("ix_nurse_profiles_nurse_id", "nurse_profiles", ["nurse_id"])

    # --- Receptionist Profiles ---
    op.create_table(
        "receptionist_profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("receptionist_id", sa.String(50), unique=True),
    )

    # --- Audit Logs ---
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(255)),
        sa.Column("timestamp", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])

    # --- Twilio Logs ---
    op.create_table(
        "twilio_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),  # sms, call, fax
        sa.Column("direction", sa.String(20), nullable=False),  # inbound/outbound
        sa.Column("from_number", sa.String(20)),
        sa.Column("to_number", sa.String(20)),
        sa.Column("content", sa.Text),
        sa.Column("status", sa.String(50)),
        sa.Column("timestamp", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_twilio_logs_type", "twilio_logs", ["type"])
    op.create_index("ix_twilio_logs_timestamp", "twilio_logs", ["timestamp"])


def downgrade():
    op.drop_table("twilio_logs")
    op.drop_table("audit_logs")
    op.drop_table("receptionist_profiles")
    op.drop_table("nurse_profiles")
    op.drop_table("doctor_notes")
    op.drop_table("appointments")
    op.drop_table("patients")
    op.drop_table("users")
    op.drop_table("roles")
