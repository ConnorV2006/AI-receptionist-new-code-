"""Add useful indexes for common queries

Revision ID: 0010_add_indexes
Revises: 0009_seed_notes
Create Date: 2025-10-03
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "0010_add_indexes"
down_revision = "0009_seed_notes"
branch_labels = None
depends_on = None


def upgrade():
    # Appointments (schedule/day views, lookups by doctor/patient)
    op.create_index("ix_appointments_scheduled_time", "appointments", ["scheduled_time"])
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"])
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])

    # Doctor notes (charting by patient/doctor, recency)
    op.create_index("ix_doctor_notes_patient_id", "doctor_notes", ["patient_id"])
    op.create_index("ix_doctor_notes_doctor_id", "doctor_notes", ["doctor_id"])
    op.create_index("ix_doctor_notes_created_at", "doctor_notes", ["created_at"])

    # Nurse profiles (lookups by nurse)
    op.create_index("ix_nurse_profiles_nurse_id", "nurse_profiles", ["nurse_id"])

    # Audit logs (filter by user / recent activity)
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])

    # Patients (directory/search; email lookups)
    op.create_index("ix_patients_last_name", "patients", ["last_name"])
    op.create_index("ix_patients_email", "patients", ["email"])

    # Optional: if you frequently filter Users by role or created_at
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_created_at", "users", ["created_at"])


def downgrade():
    # Users
    op.drop_index("ix_users_created_at", table_name="users")
    op.drop_index("ix_users_role_id", table_name="users")

    # Patients
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_index("ix_patients_last_name", table_name="patients")

    # Audit logs
    op.drop_index("ix_audit_logs_timestamp", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")

    # Nurse profiles
    op.drop_index("ix_nurse_profiles_nurse_id", table_name="nurse_profiles")

    # Doctor notes
    op.drop_index("ix_doctor_notes_created_at", table_name="doctor_notes")
    op.drop_index("ix_doctor_notes_doctor_id", table_name="doctor_notes")
    op.drop_index("ix_doctor_notes_patient_id", table_name="doctor_notes")

    # Appointments
    op.drop_index("ix_appointments_patient_id", table_name="appointments")
    op.drop_index("ix_appointments_doctor_id", table_name="appointments")
    op.drop_index("ix_appointments_scheduled_time", table_name="appointments")
