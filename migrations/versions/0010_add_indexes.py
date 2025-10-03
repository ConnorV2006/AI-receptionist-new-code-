"""Add useful indexes for common queries (concurrent)

Revision ID: 0010_add_indexes
Revises: 0009_seed_notes
Create Date: 2025-10-03
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "0010_add_indexes"
down_revision = "0009_seed_notes"
branch_labels = None
depends_on = None


def upgrade():
    # Use autocommit_block so each CREATE INDEX can run CONCURRENTLY (outside a transaction)
    with op.get_context().autocommit_block():
        # Appointments
        op.create_index(
            "ix_appointments_scheduled_time",
            "appointments",
            ["scheduled_time"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_appointments_doctor_id",
            "appointments",
            ["doctor_id"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_appointments_patient_id",
            "appointments",
            ["patient_id"],
            postgresql_concurrently=True,
        )

        # Doctor notes
        op.create_index(
            "ix_doctor_notes_patient_id",
            "doctor_notes",
            ["patient_id"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_doctor_notes_doctor_id",
            "doctor_notes",
            ["doctor_id"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_doctor_notes_created_at",
            "doctor_notes",
            ["created_at"],
            postgresql_concurrently=True,
        )

        # Nurse profiles
        op.create_index(
            "ix_nurse_profiles_nurse_id",
            "nurse_profiles",
            ["nurse_id"],
            postgresql_concurrently=True,
        )

        # Audit logs
        op.create_index(
            "ix_audit_logs_user_id",
            "audit_logs",
            ["user_id"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_audit_logs_timestamp",
            "audit_logs",
            ["timestamp"],
            postgresql_concurrently=True,
        )

        # Patients
        op.create_index(
            "ix_patients_last_name",
            "patients",
            ["last_name"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_patients_email",
            "patients",
            ["email"],
            postgresql_concurrently=True,
        )

        # Users
        op.create_index(
            "ix_users_role_id",
            "users",
            ["role_id"],
            postgresql_concurrently=True,
        )
        op.create_index(
            "ix_users_created_at",
            "users",
            ["created_at"],
            postgresql_concurrently=True,
        )


def downgrade():
    # Drops can be in a normal transaction
    op.drop_index("ix_users_created_at", table_name="users")
    op.drop_index("ix_users_role_id", table_name="users")
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_index("ix_patients_last_name", table_name="patients")
    op.drop_index("ix_audit_logs_timestamp", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")
    op.drop_index("ix_nurse_profiles_nurse_id", table_name="nurse_profiles")
    op.drop_index("ix_doctor_notes_created_at", table_name="doctor_notes")
    op.drop_index("ix_doctor_notes_doctor_id", table_name="doctor_notes")
    op.drop_index("ix_doctor_notes_patient_id", table_name="doctor_notes")
    op.drop_index("ix_appointments_patient_id", table_name="appointments")
    op.drop_index("ix_appointments_doctor_id", table_name="appointments")
    op.drop_index("ix_appointments_scheduled_time", table_name="appointments")
