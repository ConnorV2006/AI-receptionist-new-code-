"""Initial full schema with roles, users, patients, appointments, notes, profiles, audit logs, fax, and twilio logs"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# Revision identifiers
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
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
        sa.Column("password", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow, index=True),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id"), nullable=False),
    )

    # Patients
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(120), unique=True, nullable=False),
        sa.Column("phone", sa.String(20)),
    )

    # Clinics
    op.create_table(
        "clinics",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("slug", sa.String(100), unique=True, nullable=False),
        sa.Column("twilio_number", sa.String(20)),
        sa.Column("twilio_sid", sa.String(50)),
        sa.Column("twilio_token", sa.String(100)),
    )

    # Appointments
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("scheduled_time", sa.DateTime, nullable=False, index=True),
    )

    # Doctor Notes
    op.create_table(
        "doctor_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id")),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.utcnow, index=True),
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
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(200), nullable=False),
        sa.Column("details", sa.Text),
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow, index=True),
    )

    # Fax Logs
    op.create_table(
        "fax_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sender", sa.String(100), nullable=False),
        sa.Column("recipient", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),  # sent, received, failed, scheduled
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow, index=True),
    )

    # Twilio Logs
    op.create_table(
        "twilio_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),  # sms, call, fax
        sa.Column("direction", sa.String(20), nullable=False),  # inbound / outbound
        sa.Column("from_number", sa.String(50), nullable=False),
        sa.Column("to_number", sa.String(50), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("status", sa.String(20), nullable=False),  # sent, received, failed, scheduled
        sa.Column("timestamp", sa.DateTime, default=datetime.utcnow, index=True),
    )

    # Indexes
    op.create_index("ix_patients_email", "patients", ["email"])
    op.create_index("ix_patients_last_name", "patients", ["last_name"])
    op.create_index("ix_users_created_at", "users", ["created_at"])
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_scheduled_time", "appointments", ["scheduled_time"])
    op.create_index("ix_doctor_notes_created_at", "doctor_notes", ["created_at"])
    op.create_index("ix_doctor_notes_doctor_id", "doctor_notes", ["doctor_id"])
    op.create_index("ix_doctor_notes_patient_id", "doctor_notes", ["patient_id"])
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_nurse_profiles_nurse_id", "nurse_profiles", ["nurse_id"])
    op.create_index("ix_receptionist_profiles_receptionist_id", "receptionist_profiles", ["receptionist_id"])
    op.create_index("ix_fax_logs_timestamp", "fax_logs", ["timestamp"])
    op.create_index("ix_twilio_logs_timestamp", "twilio_logs", ["timestamp"])


def downgrade():
    op.drop_table("twilio_logs")
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
